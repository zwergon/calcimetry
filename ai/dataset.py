import os.path
import torch
import random

from typing import Any, Callable, Optional, Tuple

import numpy as np
from PIL import Image

from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import check_integrity


from iapytoo.utils.config import Config

from calcimetry.dataset_api import DatasetsAPI


class CalciDataset(VisionDataset):
    """Calcimetry Dataset.
    """

    default = "1.0"

    files_list = {
        '1.0': [ 
            ('dataset.pkl', 'e614103141a608563f5a0c2a9aaf68f7')
            ]
    }

    @property
    def base_folder(self):
        return "calci-ds-" + self.version

    def __init__(
        self,
        config: Config,
        train: bool = True,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        download: bool = False,
        version: str = "default",
        host: str = 'localhost',
        port: int = 27017
    ) -> None:

        super().__init__(config.dataset, transform=transform, target_transform=target_transform)
        self.host = host
        self.port = port
        self.config = config
        if version == "default":
            self.version = CalciDataset.default
        else:
            self.version = version

        if self.version not in self.files_list:
            raise RuntimeError(f"No dataset defined with this version {self.version}")

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError("Dataset not found or corrupted. You can use download=True to download it")

        self.train = train  # training set or test set
     
        data_file = os.path.join(self.root, self.base_folder, "dataset.pkl")
        with open(data_file, 'rb') as f:
            data = np.load(f)
            targets = np.load(f)

        data = np.transpose(data, (3, 2, 1, 0))
        targets = np.expand_dims(targets, axis=1)
        print(data.shape, targets.shape)

        self.indices = self._random_split_indices(targets.shape[0])
        self.data = data[self.indices].astype(np.float32) / 255.
        self.targets = targets[self.indices].astype(np.float32)
     
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
   
        return img, target

    def __len__(self) -> int:
        return self.data.shape[0]
    
    def _random_split_indices(self, size):
        random.seed(self.config.seed) # ensure train/test are disjoint
        train_size = self.config.ratio_train_test*size
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
            fpath = os.path.join(root, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True
    
    @staticmethod
    def get_md5(filename):
        import hashlib
        with open(filename, 'rb') as f:
            jpg = f.read()
            return hashlib.md5(jpg).hexdigest()

    def download(self) -> None:
        if self._check_integrity():
            print("Files already downloaded and verified")
            return
        
        folder = os.path.join(self.root, self.base_folder)
        os.makedirs(folder, exist_ok=True)

        file_list = []

        with DatasetsAPI() as dataset_api:
            
            thumbnails = dataset_api.read(self.version)
            
            n_samples = len(thumbnails)
            for i, th in enumerate(thumbnails):
                data = np.asarray(th.jpg)
            
                if i == 0:
                    print(data.shape)
                    images = np.zeros(shape=(data.shape + (n_samples,)), dtype=data.dtype)
                    targets = np.zeros(shape=(n_samples),)
              
                images[:, : , :, i] = data
                targets[i] = th.val_1m
              
            image_file = os.path.join(folder, "dataset.pkl")
            with open(image_file, 'wb') as f:
                np.save(f, images)
                np.save(f, targets)

            file_list.append(("dataset.pkl", self.get_md5(image_file)))
    
        print("list downloaded files ", file_list)
        
