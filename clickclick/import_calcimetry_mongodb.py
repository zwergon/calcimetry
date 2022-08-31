"""
Python script to import images on the local file system to the to mongoDb
"""
import json
import re
import os
import glob
import shutil
import numpy as np
import pandas as pd

import sys
sys.path.append('..')

from calcimetry.mongo_api import MongoInfo, MongoAPI

import utils as cc

if __name__ == "__main__":

    mongo_info = MongoInfo()

    dirhead = '/work/armitagj/data/csvs/REP5/'
    drillfiles = [ f.path for f in os.scandir(dirhead) if f.is_dir() ]
    filename = 'imgs2.csv'
    mesuname = 'mesu.csv'

    french_files = ['SUG1201', 'SUG1202', 'SDZ1286']

    # location of calcimetry files fo case where mesu.csv does not exist
    calcihead = '/work/armitagj/data/Excell_and_Photos/'

    # loop through all directories on the local system
    for drill in drillfiles:

        # grab the only diretory (not always called "Photos")
        images = [ f.path for f in os.scandir(drill) if f.is_dir() ]
        csvfile = images[0] + '/' + filename
        calcifile = images[0] + '/' + mesuname

        try:
            # If the images have been processed
            if os.path.isfile(csvfile):

                # get the database DrillName from the directory name (some
                # DrillName entries have extra numbers)
                with MongoAPI(mongo_info=mongo_info) as mongo_api:
                    drillname = drill.split('/')[-1]
                    partialdrillname = f'.*{drillname}.*'
                    doc = mongo_api.db['images'].find_one({'DrillName': {'$regex' : partialdrillname}})
                    realdrillname = doc['DrillName']

                    # If the drill name is not already in the databasecd
                    if mongo_api.db['measurements'].find_one({'DrillName': realdrillname}) is None:
                        # If Renaud has already created a mesu.csv file
                        if os.path.isfile(calcifile):
                            print('exists')

                            # read file
                            df = pd.read_csv(calcifile, delimiter=';')
                            df['DrillName'] = realdrillname

                            # create the json payload
                            payload = json.loads(df.to_json(orient='records'))

                            # push it to the database
                            mongo_api.write_mesu_many(payload)

                            del df

                        # Otherwise let's create the mesu.csv file from the Excel one
                        # NOTE: I don't have the mesurement ID for now, fix this
                        # once all the data is in the database
                        else:
                            print(f'creating {drillname}')

                            # grab the csv file I create with exell2csv.py
                            excell2csved = glob.glob(calcihead +
                                                     drill.split('/')[-1] +
                                                     '/*.csv')

                            print(excell2csved)
                            df1 = pd.read_csv(excell2csved[0], sep=',')

                            # LibreOffice made a mess...
                            if drillname in french_files:
                                df2 = pd.read_csv(csvfile, sep=';', encoding='cp1252')
                            else:
                                df2 = pd.read_csv(csvfile, sep=',')
                                if len(df2.columns) != 13:
                                    df2 = pd.read_csv(csvfile, sep=';')

                            # Modify Renaud's code to create a local mesu.csv
                            # file, so that it is identical to those already
                            # created

                            # I don't have a unique ID for the measurement,
                            # fix this once the database is complete
                            id = np.nan

                            with open(calcifile, 'w') as g:
                                g.write("MeasureId;ImageId;CalciCote;CalciVals1m;CalciVals15m\n")
                                for i, row2 in df2.iterrows():
                                    imgId = row2["ImageId"]
                                    cote0 = row2["Cote0"]
                                    cote1 = row2["Cote1"]
                                    for j, row1 in df1.iterrows():
                                        c = np.rint(row1["Cote"] * 100)
                                        if cote0 <= c and c <= cote1:
                                            g.write(f'{id};{imgId};{c};'
                                                    f'{df1.iloc[j, 2]};'
                                                    f'{df1.iloc[j, 4]}\n')
                                g.close()

                            # read file back in (I know...)
                            df = pd.read_csv(calcifile, delimiter=';')
                            df['DrillName'] = realdrillname

                            # create the json payload
                            payload = json.loads(df.to_json(orient='records'))

                            # push it to the database
                            mongo_api.write_mesu_many(payload)

                            del df1, df2, df

        # print error messages so that I can try and fix them and import them
        # idividually (see notebook single_calcimetry_import.ipynb)
        except Exception as e:
            print(drill)
            print(e)