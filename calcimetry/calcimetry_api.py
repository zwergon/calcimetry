"""
calcimetry_api
====================================
API to read and write data from the MongoDB
"""

import io
import re
import gridfs
from PIL import Image  
import pandas as pd
from matplotlib.pyplot import draw_if_interactive

from calcimetry.carrot_img import CarrotImage
from calcimetry.measurement import Measurement
from calcimetry.quality import Quality
from calcimetry.polyline import Polyline
from calcimetry.mongo_api import MongoAPI, MongoInfo
from calcimetry.pipelines import image_selection_pipeline, min_max_criteria
import calcimetry.use_server as server



class CalcimetryAPI(MongoAPI):

    IMG_COL = 'images'
    JPG_COL = 'jpgs'
    MES_COL = 'measurements'
    QUA_COL = 'quality'
    

    def __init__(self, mongo_info):
        super().__init__(mongo_info)
        self.img_path = server.init()
        #print(self.img_path)


    def read_image_info(self, image_id):
        """
        Return image information
        :param image_id: Image ID
        :return: image information in a Python dict
        """
        doc = self.db[self.IMG_COL].find_one({'ImageId': image_id })
        if '_id' in doc:
            del doc['_id']
        return dict(doc)
    
    def read_image(self, image_id):
        """
        load a jpeg image from its imageid directly from mongo gridfs

        returns:
            a _CarrotImage_ object
        """
        fs = gridfs.GridFS(self.db, collection=self.JPG_COL)
        file = fs.find_one({"filename": str(image_id)})
        if file is None:
            print(f"Jpg file {image_id} not found.")
            return None
        jpg = Image.open(io.BytesIO(file.read())).convert('RGB')
        
        infos = self.get_infos(image_id)
        measurements = self.get_measurements(image_id)
       
        return CarrotImage(jpg, infos = infos, measurements=measurements)

    def read_vignette(self, image_id, center=None, dim=128):
        """return a PIL Image object with only the part of CarrotImage image_id from size dimxdim"""
        img = self.read_image(image_id)
        return img.vignette(dim, center)


    def read_image_from_server(self, image_id):
        """
        load a jpeg image from its imageid using flask webservice on islin-hdmpas1 : slow

        returns:
            a _CarrotImage_ object
        """
        doc = self.db[self.IMG_COL].find_one({'ImageId': image_id })
        drill_name = doc['DrillName']
        filename = f"{self.img_path}/calci_photos/{drill_name}/Photos/{doc['FileName']}"
        jpg = server.get_file(filename)

        infos = self.get_infos(image_id)
        measurements = self.get_measurements(image_id)
       
        return CarrotImage(jpg, infos = infos, measurements=measurements)


    def get_images_df(self, query={}):
        """
        Creates a panda dataframe from the "images" collection filtered by the given query to restrict to some image_id

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

    def get_infos(self, image_id):
        doc = self.db[self.IMG_COL].find_one({'ImageId': image_id })

       
        infos = {
            "image_id": image_id,
            "px_extent": (doc['px0'], doc['px1']),
            'w_extent': (doc['Cote0'], doc['Cote1']),
            'k_up': Polyline(doc['k_Up']),
            "k_arrow": Polyline(doc['k_Arrow']),
            'k_down': Polyline(doc['k_Down'])
        }
        return infos

    def get_drill_names(self):
        return set(self.db['images'].distinct("DrillName"))

    def get_drill_name_for_image(self, image_id):
        drill_list = []
        docs = self.db[self.IMG_COL].find({'ImageId': image_id})
        for doc in docs:
            drill_list.append(doc['DrillName'])

        return drill_list

    def get_images_id(self, drillname):
        """
        This methods returns the list of "ImageId" that belong to this drillname
        """
        img_ids = []
        docs = self.db[self.IMG_COL].find({'DrillName': drillname })
        for doc in docs:
            img_ids.append(doc['ImageId'])
            
        return img_ids

    def get_filtered_images_id(self, drillnames: list = None,  
                                  cotemin: float=None, 
                                  cotemax: float=None, 
                                  resomin: float=None, 
                                  resomax: float=None,
                                  yratmin: float=None, 
                                  yratmax: float=None, 
                                  nmesmin: int=None, 
                                  nmesmax: int=None):
        """
        This method return a list of "ImageId" that fit the following filter:
        - if all filters are None, return the whole ids for the image database
        - only image ids whose fit the selected filter options
        """
        img_ids = []

        testNone = drillnames is None and cotemin is None and cotemax is None and resomin is None and \
                   resomax is None and yratmin is None and yratmax is None and nmesmin is None and nmesmax is None

        # if no filter is given return the whole list of image ids.
        if testNone: # drillnames is None and cotes_min_max is None:
            docs = self.db[self.IMG_COL].find({})
        else:
            docs = self.db[self.IMG_COL].aggregate(
                    image_selection_pipeline(
                        drills=drillnames,
                        cotemin=cotemin,
                        cotemax=cotemax,
                        resomin=resomin,
                        resomax=resomax,
                        yratmin=yratmin,
                        yratmax=yratmax,
                        nmesmin=nmesmin,
                        nmesmax=nmesmax
                        #cotes_min_max=cotes_min_max
                        )
                )
        return [ d['ImageId'] for d in docs ]

    def get_drill_list(self):
        drill_list = set()

        p = re.compile("(\S\S\S)\d*")
        for drill in self.db[self.IMG_COL].distinct("DrillName"):
            m = p.match(drill)
            if m is not None:
                name = m.group(1)
                drill_list.add(name)

        return drill_list

    def get_min_max_criteria(self):
        docs = self.db[self.IMG_COL].aggregate(min_max_criteria())
        if docs is not None:
            result = dict(next(docs))
            if '_id' in result:
                del result['_id']
            return result
        return None

    def get_quality(self, image_id):
        """
        Return image qualtiy information
        :param image_id: ID of image
        :return: quality metrics of image
        """
        quality = []
        docs = self.db[self.QUA_COL].find({'ImageId': image_id })
        for doc in docs:
            quality.append(
                Quality(
                    doc['ImageId'],
                    doc['focus'],
                    doc['gradient'],
                    doc['colours'],
                    doc['brisque'])
                    )
        return quality[0]  # return the first and only entry

    def get_drill_name_for_image(self, image_id):
        drill_list = []
        docs = self.db[self.IMG_COL].find({'ImageId': image_id})
        for doc in docs:
            drill_list.append(doc['DrillName'])

        return drill_list

    def get_selected_images_df(self, drillnames: list = None):
        """
        Creates a panda dataframe from the "images" collection filtered by the given query to restrict to some image_id

        -----------
        Examples:
            df = calcimetry_api.get_images_df(query={"DrillName": "KEY1207"})

        for the whole dataframe
            df = calcimetry_api.get_images_df()

        """
        if drillnames is None or drillnames == []:
            return None

        cursor = self.db[self.IMG_COL].find({"DrillName": {"$in": drillnames}})

        # Expand the cursor and construct the DataFrame
        df = pd.DataFrame(list(cursor))
        if '_id' in df:
            del df['_id']

        return df

    def get_measurements_list(self, imageids: list = None):
        measurements = []
        docs = self.db[self.MES_COL].find({"ImageId": {"$in": imageids}})
        for doc in docs:
            measurements.append(
                Measurement(
                    doc['ImageId'],
                    doc['MeasureId'],
                    doc['CalciCote'],
                    doc['CalciVals1m'],
                    doc['CalciVals15m'])
                    )
        return measurements

    def get_measurements(self, image_id):
       return self.get_measurements_list(imageids=[image_id])
