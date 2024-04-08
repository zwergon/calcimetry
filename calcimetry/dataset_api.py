import io
import gridfs

from calcimetry.mongo_api import MongoAPI, MongoInfo
from calcimetry.calcimetry_api import CalcimetryAPI
from PIL import Image

from calcimetry.thumbnail import Thumbnail
from calcimetry.measurement import Measurement


class DatasetsAPI(MongoAPI):
    DATASET_COL = "datasets"

    def __init__(self, mongo_info: MongoInfo = MongoInfo()):
        super().__init__(mongo_info)

    def size(self):
        return self.db[self.DATASET_COL].count_documents({})

    def read(self, version):
        docs = self.db[self.DATASET_COL].find({"version": version})
        thumbnails = [Thumbnail.from_dict(dict(d)) for d in docs]
        return thumbnails

    def read_random(self, version, limit=10):
        docs = self.db[self.DATASET_COL].aggregate(
            [{"$match": {"version": version}}, {"$sample": {"size": limit}}]
        )
        thumbnails = [Thumbnail.from_dict(dict(d)) for d in docs]
        return thumbnails
