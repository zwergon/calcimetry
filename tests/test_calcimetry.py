import unittest
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo

import matplotlib.pyplot as plt

class CalcimetryTest(unittest.TestCase):

    HOST='localhost'
    PORT=27017
    IMG_ID = 1

    def test_read_info(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            infos = calcimetry_api.read_image_info(self.IMG_ID)
            print(infos)

    def test_read_image(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image(self.IMG_ID)
            print(f"resolution : {img.resolution}")
            plt.imshow(img.jpg)
            plt.show()

    def test_read_image_from_server(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image_from_server(self.IMG_ID)
            print(f"resolution : {img.resolution}")
            plt.imshow(img.jpg)
            plt.show()
                
    def test_get_drill_list(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            print(calcimetry_api.get_drill_list())

    def test_get_drill_names(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            print(calcimetry_api.get_drill_names())

    
    def test_get_images_df(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            df = calcimetry_api.get_images_df({"DrillName": "KEY1207"})
            print(df.head())

    def test_get_resolution(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            resolution = calcimetry_api.get_resolution(self.IMG_ID)
            print(resolution)

    def test_get_vignette(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            vignette = calcimetry_api.read_vignette(self.IMG_ID)
            vignette.show()

    def test_get_measurements(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            measurements = calcimetry_api.get_measurements_from_image(self.IMG_ID)
            for m in measurements:
                print(m)


if __name__ == '__main__':
    unittest.main()