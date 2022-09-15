import glob
import os
import pandas as pd
from calcimetry.mongo_api import MongoInfo
from calcimetry.calcimetry_api import CalcimetryAPI
import gridfs

def to_polyline(param):
    if "{" in str(param) and "}" in str(param):
        t = param.replace("{", "").replace("}", "").split(";")
        return [[int(t[2*i]), int(t[2*i+1]) ]for i in range(len(t)//2)]
    else:
        return []

def push_image(api, image_id, path):
    
    fs = gridfs.GridFS(api.db, collection='jpgs')
    file = fs.find_one({"filename": str(image_id)})
    if file is None:
        with open(path, 'rb') as f:
            contents = f.read()
        fs.put(contents, filename=str(image_id))
    else:
        print(f"image {image_id} already in database")



def parse_imgs2(api, f, drillname):
    docs = []
    print(f'find imgs2 {os.path.dirname(f)}')
    df = pd.read_csv(f, encoding='cp1252', sep=';')
    for _, row in df.iterrows():
        doc = dict(row)
        #doc['_id'] = doc["ImageId"]
        doc['DrillName'] = drillname
        doc['k_Up'] = to_polyline(doc['k_Up'])
        doc['k_Down'] = to_polyline(doc['k_Down'])
        doc['k_Arrow'] = to_polyline(doc['k_Arrow'])
        del doc['Path']
        #del doc['ImageId']
        docs.append(doc)
        push_image(api, doc['ImageId'], os.path.join(os.path.dirname(f), doc["FileName"]))

    return docs


def parse_mesu(api, f):
    columns = ['MeasureId', "ImageId", "CalciCote", "CalciVals1m", "CalciVals15m"] # should be better to use bson encoder
    docs = []
    print(f'find mesu in {os.path.dirname(f)}')
    df = pd.read_csv(f, encoding='cp1252', sep=';')
    for _, row in df.iterrows():
        doc = dict(row)
        for col in columns:
            value = int(doc[col])
            doc[col] = value
        docs.append(doc)
        
    return docs



def get_drill_names(root_dir):
    drill_names = []
    for f in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, f)):
            drill_names.append(f)

    return drill_names




if __name__ == '__main__':
    root_dir = 'Z:\Images\ANDRA\BigBDD'

    mongo_info = MongoInfo(host='localhost', port=27010)

    drill_names = get_drill_names(root_dir=root_dir)
   
    with CalcimetryAPI(mongo_info=mongo_info) as mongo_api:
        for i, drill_name in enumerate(drill_names):
            imgs2_file = os.path.join(root_dir, drill_name, "Photos\imgs2.csv")
            docs = parse_imgs2(mongo_api, imgs2_file, drillname=drill_name)
            mongo_api.write_img_many(docs)

            mesu_file = os.path.join(root_dir, drill_name, "Photos\mesu.csv")
            docs = parse_mesu(mongo_api, mesu_file)
            mongo_api.write_mesu_many(docs)
           
