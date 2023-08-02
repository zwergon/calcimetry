import json
from calcimetry.meta_singleton import MetaSingleton

class Config(object, metaclass=MetaSingleton):
    CONFIG = {
        "mongo": {
            "host": "localhost",
            "port": 27017
        }
    }

    @staticmethod
    def load_from_dict(dict):
        Config.CONFIG.update(dict)
        
    
    @staticmethod
    def load_from_file(ini_file=None):
        if ini_file is not None:
            with open(ini_file, "r") as fp:
                dict = json.loads(fp.read())
                Config.load_from_dict(dict)

    @property
    def MONGO_HOST(self):
        return self.CONFIG['mongo']['host']

    @property
    def MONGO_PORT(self):
        return self.CONFIG['mongo']['port']
    