"""
Python script to import images on the local file system to the to mongoDb
"""
import json
import re
import os
import numpy as np
import pandas as pd

import sys
sys.path.append('..')

from calcimetry.mongo_api import MongoInfo, MongoAPI

import utils as cc

if __name__ == "__main__":

    mongo_info = MongoInfo()

    dirhead = '/work/armitagj/data/csvs/REP4/'
    drillfiles = [ f.path for f in os.scandir(dirhead) if f.is_dir() ]
    filename = 'imgs2.csv'

    # loop through all directories on the local system
    for drill in drillfiles:

        # grab the only diretory (not always called "Photos")
        images = [ f.path for f in os.scandir(drill) if f.is_dir() ]
        drillname = drill.split('/')[-1]
        csvfile = images[0] + '/' + filename

        try:
            # because Renaud and I don't use the same software the csv files
            # are not the same... so there are a few options (see also the
            # notebook single_image_import.ipynb)

            #df = pd.read_csv(csvfile, delimiter=';', encoding='cp1252')
            df = pd.read_csv(csvfile, delimiter=',')
            if len(df.columns) != 13:
                df = pd.read_csv(csvfile, delimiter=';')

            if len(df.columns) == 13:
                df = df.drop(columns=['Path'])

                # convert the coordinates into a list for mongodb
                df['k_Up'] = df['k_Up'].str.replace(r'{', '', regex=True)
                df['k_Up'] = df['k_Up'].str.replace(r'}', '', regex=True)
                df['k_Up'] = df['k_Up'].str.replace(r';', ',', regex=True)

                df['k_Down'] = df['k_Down'].str.replace(r'{', '', regex=True)
                df['k_Down'] = df['k_Down'].str.replace(r'}', '', regex=True)
                df['k_Down'] = df['k_Down'].str.replace(r';', ',', regex=True)

                df['k_Arrow'] = df['k_Arrow'].str.replace(r'{', '', regex=True)
                df['k_Arrow'] = df['k_Arrow'].str.replace(r'}', '', regex=True)
                df['k_Arrow'] = df['k_Arrow'].str.replace(r';', ',', regex=True)

                df['k_Up'] = df['k_Up'].apply(
                    lambda x: np.array(x.split(','), dtype=int).reshape(-1, 2)  if(pd.notnull(x)) else x)
                df['k_Down'] = df['k_Down'].apply(
                    lambda x: np.array(x.split(','), dtype=int).reshape(-1, 2)  if(pd.notnull(x)) else x)
                df['k_Arrow'] = df['k_Arrow'].apply(
                    lambda x: np.array(x.split(','), dtype=int).reshape(-1, 2)  if(pd.notnull(x)) else x)

                # create the json payload
                payload = json.loads(df.to_json(orient='records'))

                # push it to the database if the dirll name is not already
                # there
                with MongoAPI(mongo_info=mongo_info) as mongo_api:
                    if mongo_api.db['images'].find_one(
                            {'DrillName': df['DrillName'][0]}) is None:
                        print(f'importing {drillname}')
                        mongo_api.write_img_many(payload)

        # print error messages so I can try and fix them and import them
        # idividually
        except Exception as e:
            print(images)
            print(e)