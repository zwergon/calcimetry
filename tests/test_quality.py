import unittest
import os
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo
from calcimetry.quality import Quality
from calcimetry.config import Config

class QualityTest(unittest.TestCase):
    
    IMG_ID = 0

    config_file = os.path.join( os.path.dirname(__file__), "config_test.json")

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        Config.load_from_file(self.config_file)
        self.mongo_info = MongoInfo()
        
    def test_quality(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calci_api:
            img = calci_api.read_image(self.IMG_ID)
            quality = Quality(img.jpg)
            quality.compute()
            print(quality)


if __name__ == "__main__":
    unittest.main()