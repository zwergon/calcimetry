import unittest
import os
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo
from calcimetry.measurement import Measurement
from calcimetry.config import Config

import matplotlib.pyplot as plt

class CalcimetryTest(unittest.TestCase):

  
    IMG_ID = 0

    config_file = os.path.join( os.path.dirname(__file__), "config_test.json")


    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        Config.load_from_file(self.config_file)
        self.mongo_info = MongoInfo()

    def test_read_image_info(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            infos = calcimetry_api.read_image_info(self.IMG_ID)
            print(infos)

    def test_read_image(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image(self.IMG_ID)
            print(f"resolution : {img.resolution}")
            print(f"n_measurements: {img.n_measurements}")
            plt.imshow(img.jpg)
            plt.show()

    # def test_read_image_from_server(self):
    #     mongo_info = MongoInfo(host=Config.HOST, port=Config.PORT)
    #     with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
    #         img = calcimetry_api.read_image_from_server(1)
    #         print(f"resolution : {img.resolution}")
    #         plt.imshow(img.jpg)
    #         plt.show()
                
    def test_get_drill_list(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            print(calcimetry_api.get_drill_list())

    def test_get_drill_names(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            print(calcimetry_api.get_drill_names())

    
    def test_get_images_df(self):
       
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            df = calcimetry_api.get_images_df({"ImageId": {"$in": [0, 1, 2, 3]}})
            print(df.head())

    def test_get_infos(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            infos = calcimetry_api.get_infos(self.IMG_ID)
            print(infos)

    def test_get_vignette(self):
       
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            vignette = calcimetry_api.read_vignette(self.IMG_ID)
            vignette.show()

    def test_get_measurements(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            measurements = calcimetry_api.get_measurements(self.IMG_ID)
            for m in measurements:
                print(m)

    def test_get_y_ratio(self):
       
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image(self.IMG_ID)
            print(img.y_ratio)

    def test_filtered_images(self):
        drillnames = ["BPE4023", "SUG1101"]
        cotes_min_max = [100, 300]
       
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            image_ids = calcimetry_api.get_filtered_images_id()
            print(len(image_ids))
            image_ids = calcimetry_api.get_filtered_images_id(drillnames=drillnames)
            print(len(image_ids))
            image_ids = calcimetry_api.get_filtered_images_id(cotemin=cotes_min_max[0], cotemax=cotes_min_max[1])
            print(len(image_ids))
            image_ids = calcimetry_api.get_filtered_images_id(
                drillnames=drillnames,
                cotemin=cotes_min_max[0], 
                cotemax=cotes_min_max[1]
                )
            print(image_ids)

    def test_vignette_from_cote(self):
        dim = 128
       
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
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

    def test_min_max_criteria(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            mini_maxi = calcimetry_api.get_min_max_criteria()
            print(mini_maxi)

    def test_resolution(self):
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image(self.IMG_ID)
            print(img.resolution)

            plt.figure(figsize=(12, 8), dpi=80)
            #plt.imshow(img.jpg)
            #if not img.k_arrow.empty:
            #    arrow_line = draw_line(img.k_arrow)
            #    plt.gca().add_patch(arrow_line)

            zoomed_img = img.to_resolution(0.035)
            print(zoomed_img.jpg.size)
            plt.imshow(zoomed_img.jpg)
            plt.show()

    def test_vignette_outside(self):
        dim = 128
        
        with CalcimetryAPI(mongo_info=self.mongo_info) as calcimetry_api:
            img = calcimetry_api.read_image(self.IMG_ID)
            print(img.jpg.size)
            px =  3200
            center = (
                px, # get for this picture the position in pixel from this measure, shift of half of the size
                img.k_arrow.p_y(px) # get on k_arrow line the position in pixel from this measure
                )
            vignette = img.vignette(center=center, dim=dim)
            print(vignette.size)
            plt.imshow(vignette)
            plt.show()


if __name__ == '__main__':
    unittest.main()