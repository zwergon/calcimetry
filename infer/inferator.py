import os
import random
import mlflow
from PIL import Image
import numpy as np
import pandas as pd
from joblib import load

from calcimetry.quality import Quality
from sklearn.ensemble import RandomForestRegressor


class Inferfator:

    @staticmethod
    def create_inferators(filename, coords):
        return [DeepInferator(filename, coords), MLInferator(filename, coords)]

    @property
    def name(self):
        return self._kind

    def get_bbox(self, c):
        half_size = self.thumbnail_size // 2
        return (
            c[0] - half_size,
            c[0] + half_size,
            c[1] - half_size,
            c[1] + half_size,
        )

    def __init__(self, kind, filename: str, coords: list, thumbnail_size: int) -> None:
        self._kind = kind
        self.filename = filename
        self.coords = coords
        self.thumbnail_size = thumbnail_size
        self.calcimetries = []
        self.thumbnails = []

    def compute(self):
        pass


class DeepInferator(Inferfator):

    THUMBNAIL_SIZE = 48
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "static/models/deep")

    def __init__(self, filename: str, coords: list) -> None:
        super().__init__(
            "Deep", filename, coords, thumbnail_size=DeepInferator.THUMBNAIL_SIZE
        )

    def extract_thumbnails(self):
        self.thumbnails = []
        img = Image.open(self.filename).convert("RGB")
        # adjust shape and normalize need something like (3, width, height) with 0 < rgb < 1.
        array = np.transpose(np.array(img), (2, 1, 0)) / 255.0
        for c in self.coords:
            left, right, top, bottom = self.get_bbox(c)
            thumbnail = array[:, left:right, top:bottom]
            self.thumbnails.append(thumbnail)

    def compute(self):
        self.extract_thumbnails()
        model = mlflow.pyfunc.load_model(self.MODEL_PATH)

        X = np.zeros(
            shape=(len(self.thumbnails), 3, self.THUMBNAIL_SIZE, self.THUMBNAIL_SIZE),
            dtype=np.float32,
        )

        for i, th in enumerate(self.thumbnails):
            X[i, :, :, :] = th

        predictions = model.predict(X)
        for i in range(predictions.shape[0]):
            self.calcimetries.append(int(predictions[i, 0] * 100))


class MLInferator(Inferfator):

    THUMBNAIL_SIZE = 64
    NBINS = 6
    MODEL_PATH = os.path.join(
        os.path.dirname(__file__), "static/models/ml/random_forest.joblib"
    )

    stats = {
        "focus": (184.095750147647, 208.5118795424236),
        "mean_grad": (35.16229599931437, 10.959039389214787),
        "std_color": (33.9491830343596, 10.2485882445443),
        "mean_color": (112.52448201735804, 26.030479152444197),
        "brisque": (26.98129460178905, 12.182905687055118),
        "bin_0": (0.0565130840495935, 0.050103726084694),
        "bin_1": (0.1290921980551131, 0.1708091888200103),
        "bin_2": (0.3477120826868684, 0.4407420789018297),
        "bin_3": (0.8544172612141641, 0.5707595863782892),
        "bin_4": (1.2192534059548, 0.6367051731170242),
        "bin_5": (0.3930119680394607, 0.4803102740716121),
    }

    def __init__(self, filename: str, coords: list) -> None:
        super().__init__(
            "ML", filename, coords, thumbnail_size=MLInferator.THUMBNAIL_SIZE
        )

        self.columns = ["focus", "mean_grad", "std_color", "mean_color", "brisque"]
        for i in range(self.NBINS):
            self.columns.append(f"bin_{i}")

    def compute_features(self):
        data = []
        for img in self.thumbnails:
            w, h = img.size

            quality = Quality(img)
            quality.compute()
            row = [
                quality.focus,
                quality.gradient["ave"],
                np.std(quality.colours),
                np.mean(quality.colours),
                quality.brisque,
            ]

            # add histogram values
            histo, _ = np.histogram(img, bins=self.NBINS)
            histo = histo.astype(np.float64) / (w * h)
            for i in range(self.NBINS):
                val = float(histo[i]) / (w * h)
                row.append(val)

            data.append(row)

        return pd.DataFrame(data, columns=self.columns)

    def extract_thumbnails(self):
        self.thumbnails = []
        img = Image.open(self.filename)

        for c in self.coords:
            left, right, top, bottom = self.get_bbox(c)
            thumbnail = img.crop([left, top, right, bottom])
            self.thumbnails.append(thumbnail)

    def compute(self):
        self.extract_thumbnails()
        df = self.compute_features()

        for c in df.columns:
            mean_std = self.stats[c]
            df[c] = (df[c] - mean_std[0]) / mean_std[1]

        model = load(MLInferator.MODEL_PATH)
        y = model.predict(df)
        for i in range(y.shape[0]):
            self.calcimetries.append(y[i])
