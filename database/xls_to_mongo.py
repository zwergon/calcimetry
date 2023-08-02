import glob
import os
import pandas as pd
from calcimetry.mongo_api import MongoInfo
from calcimetry.calcimetry_api import CalcimetryAPI
import gridfs
from calcimetry.config import Config

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



def parse_imgs2(f, drillname):
    docs = []
    print(f'..find imgs2 {os.path.dirname(f)}')
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
        
    return docs

def push_jpgs(api, f):
    print(f"..push jpg images from {os.path.dirname(f)}")
    df = pd.read_csv(f, encoding='cp1252', sep=';')
    for _, row in df.iterrows():
        doc = dict(row)
        push_image(api, doc['ImageId'], os.path.join(os.path.dirname(f), doc["FileName"]))


def parse_mesu(f):
    columns = ['MeasureId', "ImageId", "CalciCote", "CalciVals1m", "CalciVals15m"] # should be better to use bson encoder
    docs = []
    print(f'..find mesu in {os.path.dirname(f)}')
    df = pd.read_csv(f, encoding='cp1252', sep=';')
    for _, row in df.iterrows():
        doc = dict(row)
        for col in columns:
            value = int(doc[col])
            doc[col] = value
        docs.append(doc)
        
    return docs


def get_drill_names(root_dir):
    """create a set of drillnames from directories"""
    drill_names = set()
    for f in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, f)):
            drill_names.add(f)

    return drill_names


if __name__ == '__main__':

    import argparse

    
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Path to directory of BDD", default='Z:\Images\ANDRA\BigBDD')
    parser.add_argument("-ho", "--host", help="host pour la base mongodb", default='localhost')
    parser.add_argument("-p", "--port", default=27017, type=int, help="port pour accéder à la base mongodb")
    parser.add_argument('--jpg', dest='jpgs', action='store_true')
    parser.add_argument('--no-jpg', dest='jpgs', action='store_false')
    parser.set_defaults(feature=True)

    args = parser.parse_args()

    config = Config.load_from_dict(
        {
            "mongo": {
                "host": args.host,
                "port": args.port
            }
        }
    )

    mongo_info = MongoInfo(config=config)

    drill_names = get_drill_names(root_dir=args.dir)
    print(f"there are {len(drill_names)} to import from directories")
   
    with CalcimetryAPI(mongo_info=mongo_info) as mongo_api:

        print("push imgs2 & mesu")
        already_in_names = mongo_api.get_drill_names()
        to_add_names = drill_names - already_in_names
        print(f".only {len(to_add_names)} after removal of drills already in db")

        for i, drill_name in enumerate(to_add_names):
            imgs2_file = os.path.join(args.dir, drill_name, "Photos\imgs2.csv")
            docs = parse_imgs2(imgs2_file, drillname=drill_name)
            mongo_api.write_img_many(docs)

            mesu_file = os.path.join(args.dir, drill_name, "Photos\mesu.csv")
            docs = parse_mesu(mesu_file)
            if len(docs) > 0:
                mongo_api.write_mesu_many(docs)
            else:
                print(f"it seems there are no measurements in {drill_name}")


        if args.jpgs:
            print("push jpgs...")
            for i, drill_name in enumerate(drill_names):
                imgs2_file = os.path.join(args.dir, drill_name, "Photos\imgs2.csv")
                push_jpgs(mongo_api, imgs2_file)