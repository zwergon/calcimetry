from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo
from calcimetry.carrot_img import CarrotImage
import matplotlib.pyplot as plt

def display_img(mongo_info, img_id):
    with CalcimetryAPI(mongo_info=mongo_info) as calci_api:
        img = calci_api.read_image(image_id=img_id)
        img.jpg.show()

def update_criteria(mongo_info):
    
    with CalcimetryAPI(mongo_info=mongo_info) as calci_api:
        image_ids = calci_api.get_filtered_images_id()
        for img_id in image_ids:
            img = calci_api.read_image(image_id=img_id)
            if img is not None:
                print(f"handle image {img_id}")
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
    mongo_info = MongoInfo(host='localhost', port='27010')
    update_criteria(mongo_info=mongo_info)
    #display_img(mongo_info, 1157)