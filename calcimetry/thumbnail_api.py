import io
import gridfs

from calcimetry.mongo_api import MongoAPI, MongoInfo
from calcimetry.calcimetry_api import CalcimetryAPI
from PIL import Image

from calcimetry.thumbnail import Thumbnail  
from calcimetry.measurement import Measurement

class ThumbnailAPI(MongoAPI):

    THU_COL = 'vignettes'

    def __init__(self, mongo_info: MongoInfo):
        super().__init__(mongo_info)
        
    def size(self):
        return self.db[self.THU_COL].count_documents({})

    def read(self, thu_id):
        doc = self.db[self.THU_COL].find_one({'ThuId': thu_id })
        if doc is None:
            print(f"Thumbnail {thu_id} not found.")
            return None
        th_dict = dict(doc)
        thumbnail = Thumbnail.from_dict(th_dict)
        doc = self.db[CalcimetryAPI.MES_COL].find_one({'MeasureId': th_dict['measurement']})
        if doc is not None:
            thumbnail.measurement =  Measurement(
                                        doc['ImageId'],
                                        doc['MeasureId'],
                                        doc['CalciCote'],
                                        doc['CalciVals1m'],
                                        doc['CalciVals15m']
                                        )
            
        return thumbnail