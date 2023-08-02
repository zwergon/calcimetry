import unittest
import os
from calcimetry.thumbnail_api import ThumbnailAPI
from calcimetry.mongo_api import MongoInfo
from calcimetry.config import Config

import matplotlib.pyplot as plt

class TestThumbnailAPI(unittest.TestCase):

    THU_ID = 46

    config_file = os.path.join( os.path.dirname(__file__), "config_test.json")

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        Config.load_from_file(self.config_file)
        self.mongo_info = MongoInfo()

    def test_read_image(self):
        with ThumbnailAPI(mongo_info=self.mongo_info) as thumb_api:
            thumbnail = thumb_api.read(self.THU_ID)
            print(f"val_1m: {thumbnail.measurement.val_1m}")
            print(f"brisque: {thumbnail.quality.brisque}")
            print(f"measure {thumbnail.measurement.measure_id}")
            print(f"image_id {thumbnail.image_id}")
            plt.imshow(thumbnail.jpg)
            plt.show()


if __name__ == '__main__':
    unittest.main()