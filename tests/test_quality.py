import unittest
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo
from calcimetry.quality import Quality
from config import Config

class QualityTest(unittest.TestCase):
    
    IMG_ID = 0

    def test_quality(self):
        mongo_info = MongoInfo(host=Config.HOST, port=Config.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calci_api:
            img = calci_api.read_image(self.IMG_ID)
            quality = Quality(img.jpg)
            quality.compute()
            print(quality)


if __name__ == "__main__":
    unittest.main()