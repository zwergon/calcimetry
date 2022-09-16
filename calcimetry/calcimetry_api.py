

import io
import re
import gridfs
from PIL import Image  
import pandas as pd

from calcimetry.carrot_img import CarrotImage
from calcimetry.measurement import Measurement
from calcimetry.mongo_api import MongoAPI, MongoInfo
import calcimetry.use_server as server


class CalcimetryAPI(MongoAPI):

    IMG_COL = 'images'
    JPG_COL = 'jpgs'
    MES_COL = 'measurements'
    

    def __init__(self, mongo_info):
        super().__init__(mongo_info)
        self.img_path = server.init()
        print(self.img_path)


    def read_image_info(self, image_id):
        doc = self.db[self.IMG_COL].find_one({'ImageId': image_id })
        if '_id' in doc:
            del doc['_id']
        return dict(doc)
    
    def read_image(self, image_id):
        """
        load a jpeg image from its imageid directly from mongo gridfs
        
        -----
        returns:
            a _CarrotImage_ object
        """
        fs = gridfs.GridFS(self.db, collection=self.JPG_COL)
        file = fs.find_one({"filename": str(image_id)})
        jpg = Image.open(io.BytesIO(file.read()))
        
        return CarrotImage(jpg, resolution = self.get_resolution(image_id))

    def read_vignette(self, image_id, center=None, dim=128):
        """return a PIL Image object with only the part of CarrotImage image_id from size dimxdim"""
        img = self.read_image(image_id)
        return img.vignette(dim, center, img.resolution)


    def read_image_from_server(self, image_id):
        """
        load a jpeg image from its imageid using flask webservice on islin-hdmpas1 : slow

        ---------
        returns:
            a _CarrotImage_ object
        """
        doc = self.db[self.IMG_COL].find_one({'ImageId': image_id })
        drill_name = doc['DrillName']
        filename = f"{self.img_path}/calci_photos/{drill_name}/Photos/{doc['FileName']}"
        jpg = server.get_file(filename)

        return CarrotImage(jpg, resolution = self.get_resolution(image_id))


    def get_measurements_from_image(self, image_id):
        measurements = []
        docs = self.db[self.MES_COL].find({'ImageId': image_id })
        for doc in docs:
            measurements.append( 
                Measurement(
                    doc['MeasureId'], 
                    doc['CalciCote'], 
                    doc['CalciVals1m'], 
                    doc['CalciVals15m'])
                    )
        return measurements


    def get_images_df(self, query={}):
        """
        Creates a panda dataframe from the "images" collection filtered by the given query to restrict to some image_id

        -----------
        Examples:
            df = calcimetry_api.get_images_df(query={"DrillName": "KEY1207"})

        for the whole dataframe
            df = calcimetry_api.get_images_df()

        """
        cursor = self.db[self.IMG_COL].find(query)

        # Expand the cursor and construct the DataFrame
        df =  pd.DataFrame(list(cursor))
        if '_id' in df:
            del df['_id']

        return df

    def get_resolution(self, image_id):
        doc = self.db[self.IMG_COL].find_one({'ImageId': image_id })

        ratio = (doc['Cote1']-doc['Cote0']) /(doc['px1']-doc['px0'])

        resolution = abs(ratio)
        w_transform = (doc['Cote0'], 1. / resolution)
         
        return resolution, w_transform

    def get_drill_names(self):
        return set(self.db['images'].distinct("DrillName"))

    def get_drill_list(self):
        drill_list = set()

        p = re.compile("(\S\S\S)\d*")
        for drill in self.db[self.IMG_COL].distinct("DrillName"):
            m = p.match(drill)
            if m is not None:
                name = m.group(1)
                drill_list.add(name)

        return drill_list