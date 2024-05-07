import os
from pymongo import MongoClient


class MongoInfo:

    UNKNOWN_ID = int(-1)

    def __init__(self, db_name="calcimetry"):

        self.host = os.environ.get("MONGO_HOST", "localhost")
        self.port = os.environ.get("MONGO_PORT", 27017)
        self.db_name = db_name

    @property
    def mongo_client(self):
        return f"mongodb://{self.host}:{self.port}"


class MongoAPI:

    def __init__(self, mongo_info=MongoInfo()):
        self.mongo_info = mongo_info
        self.client = MongoClient(self.mongo_info.mongo_client)
        self.db = self.client[self.mongo_info.db_name]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.client.close()

    def write_img_one(self, doc):
        self.db["images"].insert_one(doc)

    def write_img_many(self, docs):
        self.db["images"].insert_many(docs)

    def write_mesu_one(self, doc):
        self.db["measurements"].insert_one(doc)

    def write_mesu_many(self, docs):
        self.db["measurements"].insert_many(docs)

    def write_quality_one(self, doc):
        self.db["quality"].insert_one(doc)

    def write_quality_many(self, docs):
        self.db["quality"].insert_many(docs)
