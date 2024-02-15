import unittest

import numpy as np

from iapytoo.utils.config import Config
from ai.dataset import CalciDataset
import matplotlib.pyplot as plt

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

class TestDataset(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)


    def test_dataset_api(self):
        config = Config.test_config()
        config.dataset = './tests'

        train_dataset = CalciDataset(config, download=True, version="1.0", train=True)
        print(len(train_dataset))

        test_dataset = CalciDataset(config, download=True, version="1.0", train=False)
        print(len(test_dataset))


        print(len(intersection(train_dataset.indices, test_dataset.indices)))


        img, target = train_dataset[67]
        print(img.dtype )
        plt.imshow(np.transpose(img, (2, 1, 0)))
        plt.show()
            
       


if __name__ == '__main__':
    unittest.main()