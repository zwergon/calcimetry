import unittest
from calcimetry.dataset_api import DatasetsAPI
import matplotlib.pyplot as plt
import numpy as np

class TestThumbnail(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)


    def test_dataset_api(self):
        with DatasetsAPI() as dataset_api:
            thumbnails = dataset_api.read("1.0")
            th = thumbnails[0]
            print(th.to_dict())
            
            plt.imshow(th.jpg)
            plt.show()
            
       


if __name__ == '__main__':
    unittest.main()