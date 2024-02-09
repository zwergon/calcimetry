import unittest
from ai.dataset import CalciDataset
import matplotlib.pyplot as plt

class TestDataset(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)


    def test_dataset_api(self):
        dataset = CalciDataset("./tests", download=True, version="1.0")
        print(len(dataset))

        img, target = dataset[12]
        plt.imshow(img)
        plt.show()
            
       


if __name__ == '__main__':
    unittest.main()