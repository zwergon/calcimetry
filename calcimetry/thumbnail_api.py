import io
import gridfs

from calcimetry.mongo_api import MongoAPI, MongoInfo
from PIL import Image  


class ThumbnailAPI(MongoAPI):

    FIL_COL = 'vignettes.files'
    THU_COL = 'vignettes'

    def __init__(self, mongo_info: MongoInfo):
        super().__init__(mongo_info)
        

    def size(self):
        return self.db[self.FIL_COL].count()

    def read(self, thu_id):
        fs = gridfs.GridFS(self.db, collection=self.THU_COL)
        file = fs.find_one({"filename": str(thu_id)})
        if file is None:
            print(f"Jpg file {thu_id} not found.")
            return None
        jpg = Image.open(io.BytesIO(file.read()))
        meta = file.meta
    
        return jpg, meta