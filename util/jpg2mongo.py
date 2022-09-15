
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo

import gridfs
import io


def write_img(api, image_id):
    fs = gridfs.GridFS(calcimetry_api.db, collection='jpgs')
    file = fs.find_one({"filename": str(image_id)})
    if file is None:
        print(f"import image {image_id}")
        img = api.read_image_from_server(image_id)
        output = io.BytesIO()
        img.save(output, format='jpeg')
        fs.put(output.getvalue(), filename=str(image_id))
    else:
        print(f"image {image_id} already in database")



if __name__ == "__main__":

    import matplotlib.pyplot as plt
  
    mongo_info = MongoInfo(host='localhost', port=27010)
    with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
        #for i in range(5, 10):
        #    write_img(calcimetry_api, i)

        img = calcimetry_api.read_image(569)
        plt.imshow(img)
        plt.show()
       
        
