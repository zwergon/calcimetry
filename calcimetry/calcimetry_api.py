

import io
import re
import gridfs
from PIL import Image  

from calcimetry.mongo_api import MongoAPI, MongoInfo
import calcimetry.use_server as server


class CalcimetryAPI(MongoAPI):
    

    def __init__(self, mongo_info):
        super().__init__(mongo_info)
        self.img_path = server.init()
        print(self.img_path)
    
    def read_image(self, image_id):
        """load a jpeg image from its imageid directly from mongo gridfs"""
        fs = gridfs.GridFS(self.db, collection='jpgs')
        file = fs.find_one({"filename": str(image_id)})
        print(file)
        img = Image.open(io.BytesIO(file.read()))
        return img

    def read_image_from_server(self, image_id):
        """load a jpeg image from its imageid using flask webservice on islin-hdmpas1 : slow"""
        doc = self.db['images'].find_one({'ImageId': image_id })
        drill_name = doc['DrillName']
        filename = f"{self.img_path}/calci_photos/{drill_name}/Photos/{doc['FileName']}"
        img = server.get_file(filename)

        return img

    def get_images_df(self):
        pass

    def get_drill_list(self):
        drill_list = {}

        p = re.compile("(\s\s\s)\d*")
        for drill in self.db['images'].distinct("DrillName"):
            m = p.match(drill)
            if m is not None:
                name = m.group(1)
                drill_list.add(name)

        return drill_list