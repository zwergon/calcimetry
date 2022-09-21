import unittest
from calcimetry.thumbnail_api import ThumbnailAPI
from calcimetry.mongo_api import MongoInfo
from tests.config import Config

import matplotlib.pyplot as plt

class TestThumbnailAPI(unittest.TestCase):

    THU_ID = 12

    def test_read_image(self):
        mongo_info = MongoInfo(host=Config.HOST, port=Config.PORT)
        with ThumbnailAPI(mongo_info=mongo_info) as thumb_api:
            thumb, val_1m = thumb_api.read(self.THU_ID)
            print(f"val_1m: {val_1m}")
            plt.imshow(thumb)
            plt.show()


if __name__ == '__main__':
    unittest.main()