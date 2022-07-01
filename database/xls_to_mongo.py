import glob
import os
import pandas as pd
import pymongo
from calcimetry.mongo_api import MongoInfo, MongoAPI

def to_polyline(param):
    if "{" in str(param) and "}" in str(param):
        t = param.replace("{", "").replace("}", "").split(";")
        return [[int(t[2*i]), int(t[2*i+1]) ]for i in range(len(t)//2)]
    else:
        return []


def parse_imgs2(f):
    docs = []
    print(f'find imgs2 {os.path.dirname(f)}')
    df = pd.read_csv(f, encoding='cp1252', sep=';')
    for _, row in df.iterrows():
        doc = dict(row)
        #doc['_id'] = doc["ImageId"]
        doc['k_Up'] = to_polyline(doc['k_Up'])
        doc['k_Down'] = to_polyline(doc['k_Down'])
        doc['k_Arrow'] = to_polyline(doc['k_Arrow'])
        del doc['Path']
        #del doc['ImageId']
        docs.append(doc)

    return docs


if __name__ == '__main__':
    root_dir = '../data'

    mongo_info = MongoInfo()

    for f in glob.glob(os.path.join(root_dir, "*/*/Photos/*.csv")):
        if 'imgs2.csv' in f:
            docs = parse_imgs2(f)
            with MongoAPI(mongo_info=mongo_info) as mongo_api:
                mongo_api.write_img_many(docs)

