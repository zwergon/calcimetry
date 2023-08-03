from cmath import isnan, nan
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo
from calcimetry.quality import Quality
from calcimetry.measurement import Measurement

import matplotlib.pyplot as plt

def display_img(mongo_info, img_id):
    with CalcimetryAPI(mongo_info=mongo_info) as calci_api:
        img = calci_api.read_image(image_id=img_id)
        img.jpg.show()

def update_quality(mongo_info, update=False):
     with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:

        # create a list of all image ids
        image_ids = calcimetry_api.get_filtered_images_id()
        print(len(image_ids))

        # loop through all ids
        for image_id in image_ids:
            img = calcimetry_api.read_image(image_id)

            if img is not None:

                infos = calcimetry_api.read_image_info(image_id)
                criteria = {}
                if 'criteria' in infos:
                    criteria.update(infos['criteria'])
               
                # create quality metric
                Q = Quality(img.jpg)
                Q.compute()
                criteria.update(Q.to_dict())
                
                if update:
                    print(f".update image {image_id}")
                    calcimetry_api.db[CalcimetryAPI.IMG_COL].update_one(
                        filter={"ImageId": image_id},
                        update={
                            "$set": {
                                "criteria": criteria
                            }
                        }
                    )
                

def update_criteria(mongo_info, update=False):
    
    with CalcimetryAPI(mongo_info=mongo_info) as calci_api:
        image_ids = calci_api.get_filtered_images_id()
        for img_id in image_ids:
            img = calci_api.read_image(image_id=img_id)
            if img is not None:
                #
                if isnan(img.resolution):
                    print( "nan for ", img_id)
                else:
                    print(f"handle image {img_id}")
                if update:
                    calci_api.db[CalcimetryAPI.IMG_COL].update_one(
                        filter={"ImageId": img_id},
                        update={
                            "$set": {
                                "criteria": {
                                    "n_measurements": img.n_measurements,
                                    "resolution": img.resolution,
                                    "y_ratio": img.y_ratio
                                }
                            }
                        }
                    )





if __name__ == "__main__":
    mongo_info = MongoInfo()
    #update_criteria(mongo_info=mongo_info)
    display_img(mongo_info, 10)
    #update_quality(mongo_info=mongo_info, update=True)