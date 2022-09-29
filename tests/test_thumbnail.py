import unittest
from calcimetry.thumbnail_api import ThumbnailAPI
from calcimetry.mongo_api import MongoInfo
from config import Config

import matplotlib.pyplot as plt

class TestThumbnailAPI(unittest.TestCase):

    THU_ID = 46

    def test_read_image(self):
        mongo_info = MongoInfo(host=Config.HOST, port=Config.PORT)
        with ThumbnailAPI(mongo_info=mongo_info) as thumb_api:
            thumbnail = thumb_api.read(self.THU_ID)
            print(f"val_1m: {thumbnail.measurement.val_1m}")
            print(f"brisque: {thumbnail.quality.brisque}")
            print(f"image_id {thumbnail.image_id}")
            plt.imshow(thumbnail.jpg)
            plt.show()


if __name__ == '__main__':
    unittest.main()