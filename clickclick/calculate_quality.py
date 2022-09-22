"""
Python script to measure image quality and put it in the database
"""

import io, os, sys

sys.path.append('..')

# local library of functions
from calcimetry.mongo_api import MongoInfo, MongoAPI
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.quality import Quality

# parameters where the database is stored, can obviously be distant.
# ssh -f -N -L 27017:irlinv-tellus:27017 irlinv-tellus
HOST = 'localhost'
PORT = 27017


if __name__ == '__main__':

    mongo_info = MongoInfo(host=HOST, port=PORT)
    mongo_api = MongoAPI(mongo_info=mongo_info)
    with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:

        # create a list of all image ids
        col = mongo_api.db['images'].find()
        image_ids = [row['ImageId'] for row in list(col)]

        # loop through all ids
        for image_id in image_ids:
            img = calcimetry_api.read_image(image_id)

            # create quality metric
            Q = Quality(image_id)
            Q.add_simple_metrics(img.jpg)
            Q.add_colours(img.jpg, 3)
            Q.add_brisque_index(img.jpg)

            # write quality metric to collection "quality"
            mongo_api.write_quality_one(vars(Q))