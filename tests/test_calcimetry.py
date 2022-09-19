import unittest
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo
from calcimetry.measurement import Measurement

import matplotlib.pyplot as plt

class CalcimetryTest(unittest.TestCase):

    HOST='localhost'
    PORT=27010
    IMG_ID = 1412

    def test_read_image_info(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            infos = calcimetry_api.read_image_info(self.IMG_ID)
            print(infos)

    def test_read_image(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image(self.IMG_ID)
            print(f"resolution : {img.resolution}")
            print(f"n_measurements: {img.n_measurements}")
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

    def test_get_infos(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            infos = calcimetry_api.get_infos(self.IMG_ID)
            print(infos)

    def test_get_vignette(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            vignette = calcimetry_api.read_vignette(self.IMG_ID)
            vignette.show()

    def test_get_measurements(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            measurements = calcimetry_api.get_measurements(self.IMG_ID)
            for m in measurements:
                print(m)

    def test_get_y_ratio(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image(self.IMG_ID)
            print(img.y_ratio)


    def test_vignette_from_cote(self):
        dim = 128
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image(self.IMG_ID)
            measure = img.measurements[0]
            p_x = img.p_x(measure.cote) + dim // 2
            center = (
                p_x, # get for this picture the position in pixel from this measure, shift of half of the size
                img.k_arrow.p_y(p_x) # get on k_arrow line the position in pixel from this measure
                )
            vignette = calcimetry_api.read_vignette(self.IMG_ID, center, dim=dim)
            plt.imshow(vignette)
            plt.show()


if __name__ == '__main__':
    unittest.main()