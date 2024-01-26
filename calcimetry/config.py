import os
from calcimetry.meta_singleton import MetaSingleton

class Config(object, metaclass=MetaSingleton):
   
    def __init__(self) -> None:
        self.MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
        self.MONGO_PORT = os.environ.get('MONGO_PORT', 27010)
        print(self)

    def __repr__(self) -> str:
        return f"MongoConnection : {self.MONGO_HOST}:{self.MONGO_PORT}"
