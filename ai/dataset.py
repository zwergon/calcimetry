import os.path
import logging
import random
import re

from typing import Any, Callable, Optional, Tuple

import numpy as np
from PIL import Image

from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import check_integrity


from iapytoo.utils.config import Config
from iapytoo.dataset.scaling import Scaling

from calcimetry.dataset_api import DatasetsAPI


class CalciDataset(VisionDataset):
    """Calcimetry Dataset."""

    default = "1.1"

    _pattern = re.compile(r"([\w+|\/]*)\/(\d+\.\d+)?")

    files_list = {
        "1.0": [("dataset.npz", "e614103141a608563f5a0c2a9aaf68f7")],
        # "1.1": [("dataset.npz", "ec13f8aa1d7f76fb350635d229293178")],
        "1.1": [("dataset.npz", "14af3214b8d31a122f9594902dacb1f9")],
        # "1.2": [("dataset.npz", "4efa410fe3829d680ebb59b0a44a3694")],
        "1.2": [("dataset.npz", "62b289880ccab45ab9d142fcfbce6bad")],
    }

    @staticmethod
    def version(dataset):
        m = re.search(CalciDataset._pattern, dataset)
        if m:
            return m.group(2)
        else:
            raise f"dataset {dataset} has a wrong format basename/1.0"

    def __init__(
        self,
        config: Config,
        scaling: Scaling = None,
        train: bool = True,
        download: bool = False,
        host: str = "localhost",
        port: int = 27017,
    ) -> None:
        super().__init__(config.dataset, target_transform=scaling)
        self.host = host
        self.port = port
        self.config = config

        self.version = CalciDataset.version(config.dataset)
        if self.version not in self.files_list:
            raise RuntimeError(f"No dataset defined with this version {self.version}")

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError(
                "Dataset not found or corrupted. You can use download=True to download it"
            )

        self.train = train  # training set or test set

        data_file = os.path.join(self.root, "dataset.npz")
        npzfile = np.load(data_file)
        images = npzfile["images"]
        targets = npzfile["targets"]

        images = np.transpose(images, (3, 2, 1, 0))
        targets = np.expand_dims(targets, axis=1)

        self.indices = self._random_split_indices(targets.shape[0])
        self.data = images[self.indices] / 255.0
        self.targets = targets[self.indices]

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        img, target = self.data[index], self.targets[index]

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img.astype(np.float32), target.astype(np.float32)

    def __len__(self) -> int:
        return self.data.shape[0]

    def _random_split_indices(self, size):
        random.seed(self.config.seed)  # ensure train/test are disjoint
        train_size = self.config.ratio_train_test * size
        indices = list(range(size))
        random.shuffle(indices)
        train_indices = []
        while len(train_indices) < train_size:
            train_indices.append(indices.pop())

        if self.train:
            return train_indices
        else:
            return indices

    def _check_integrity(self) -> bool:
        root = self.root

        for fentry in CalciDataset.files_list[self.version]:
            filename, md5 = fentry[0], fentry[1]
            fpath = os.path.join(root, filename)
            if not check_integrity(fpath, md5):
                return False
        return True

    @staticmethod
    def get_md5(filename):
        import hashlib

        with open(filename, "rb") as f:
            jpg = f.read()
            return hashlib.md5(jpg).hexdigest()

    def download(self) -> None:
        if self._check_integrity():
            logging.info("Files already downloaded and verified")
            return

        folder = os.path.join(self.root)
        os.makedirs(folder, exist_ok=True)

        file_list = []

        with DatasetsAPI() as dataset_api:
            thumbnails = dataset_api.read(self.version)

            n_samples = len(thumbnails)
            for i, th in enumerate(thumbnails):
                data = np.asarray(th.jpg)

                if i == 0:
                    images = np.zeros(
                        shape=(data.shape + (n_samples,)), dtype=data.dtype
                    )
                    targets = np.zeros(
                        shape=(n_samples),
                    )

                images[:, :, :, i] = data
                targets[i] = th.val_1m

            dct = {"images": images, "targets": targets}
            image_file = os.path.join(folder, "dataset.npz")
            np.savez(image_file, **dct)

            file_list.append(("dataset.npz", self.get_md5(image_file)))

        logging.info(f"list downloaded files {file_list}")
