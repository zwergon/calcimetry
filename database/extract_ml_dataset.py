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
                for m in img.measurements:
                    if img.k_arrow.empty:
                        continue
                    p_x = img.p_x(m.cote)
                    center = (
                        p_x, # get for this picture the position in pixel from this measure, shift of half of the size
                        img.k_arrow.p_y(p_x) # get on k_arrow line the position in pixel from this measure
                        )
                    vignette = calci_api.read_vignette(img_id, center, dim=dim)
                    if vignette_id is not None:
                        img_byte_array = io.BytesIO()
                        vignette.save(img_byte_array, format='jpeg')
                        fs.put(img_byte_array.getvalue(), filename=str(vignette_id), meta=m.val_1m)
                        vignette_id += 1
    


if __name__ == "__main__":
    mongo_info = MongoInfo(host='localhost', port='27010')
    extract_dataset(mongo_info=mongo_info)