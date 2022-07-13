from pymongo import MongoClient

class MongoInfo:

    UNKNOWN_ID = int(-1)

    # client = MongoClient('mongodb://irlinv-dvbacr16:7017')
    HOST = 'irlinv-dvbacr16'
    PORT = 7017

    def __init__(self,
                 host=HOST,
                 port=PORT,
                 db_name='calcimetry'
                 ):
        self.host = host
        self.port = port
        self.db_name = db_name

    @property
    def mongo_client(self):
        return f"mongodb://{self.host}:{self.port}"


class MongoAPI:

    def __init__(self, mongo_info):
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
        self.db['images'].insert_one(doc)

    def write_img_many(self, docs):
        self.db['images'].insert_many(docs)