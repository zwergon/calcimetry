import os
import random
import mlflow
from PIL import Image
import numpy as np


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
        pass


class DeepInferator(Inferfator):

    THUMBNAIL_SIZE = 48
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "assets/models/deep")

    def __init__(self, filename: str, coords: list) -> None:
        super().__init__(
            "Deep", filename, coords, thumbnail_size=DeepInferator.THUMBNAIL_SIZE
        )

    def compute(self):
        self.extract_thumbnails()
        print(self.MODEL_PATH)
        model = mlflow.pyfunc.load_model(self.MODEL_PATH)

        X = np.zeros(
            shape=(len(self.thumbnails), 3, self.THUMBNAIL_SIZE, self.THUMBNAIL_SIZE),
            dtype=np.float32,
        )

        for i, th in enumerate(self.thumbnails):
            X[i, :, :, :] = th

        predictions = model.predict(X)
        print(predictions.shape)
        for i in range(predictions.shape[0]):
            self.calcimetries.append(int(predictions[i, 0] * 100))


class MLInferator(Inferfator):

    THUMBNAIL_SIZE = 64

    def __init__(self, filename: str, coords: list) -> None:
        super().__init__(
            "ML", filename, coords, thumbnail_size=MLInferator.THUMBNAIL_SIZE
        )

    def compute(self):
        self.extract_thumbnails()
        for th in self.thumbnails:
            calci = random.uniform(50, 100)
            self.calcimetries.append(calci)
