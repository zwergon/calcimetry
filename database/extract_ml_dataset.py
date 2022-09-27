from calcimetry.mongo_api import MongoInfo
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.measurement import Measurement
import gridfs
import io

def extract_dataset(mongo_info, dim=128):

    vignette_id = 0
    with CalcimetryAPI(mongo_info=mongo_info) as calci_api:
        fs = gridfs.GridFS(calci_api.db, collection='vignettes')
        image_ids = calci_api.get_filtered_images_id()
        for img_id in image_ids:
            img = calci_api.read_image(image_id=img_id)
            if img is not None:
                img = img.to_resolution(0.035)
                for m in img.measurements:
                    if img.k_arrow.empty:
                        continue
                    p_x = img.p_x(m.cote)
                    center = (
                        p_x, # get for this picture the position in pixel from this measure, shift of half of the size
                        img.k_arrow.p_y(p_x) # get on k_arrow line the position in pixel from this measure
                        )
                    vignette = img.vignette(center=center, dim=dim)
                    if vignette_id is not None:
                        img_byte_array = io.BytesIO()
                        vignette.save(img_byte_array, format='jpeg')
                        fs.put(img_byte_array.getvalue(), 
                            filename=str(vignette_id), 
                            meta= {
                                "val_1m": m.val_1m,
                                "ImageID": img_id
                                }
                            )
                        vignette_id += 1
    


if __name__ == "__main__":
    mongo_info = MongoInfo(host='localhost', port='27017')
    extract_dataset(mongo_info=mongo_info)