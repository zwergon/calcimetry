"""
Python script to create the database. If the dataframe does nto exist,
it will save it as Andra_data.pkl. If it does exist it will use it to save
the individual drill data as csv files next to the Excell data.
"""
import os
import argparse
import pandas as pd
import utils as cc

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", required=True,
                    help="Path to directory of excell files")
    args = vars(ap.parse_args())
    dirName = args["directory"]

    # Go into the directory tree and exract the excell files to create csv
    # equivalents that are clean and ready to be associated with images
    cc.calcimetry.excell2csv(dirName)

    # Go into each directory on the image server and create both a database
    # and individual csv files of the image properties prior to clicking

    # initiate the server connection
    img_path = cc.use_server.init()

    # get a list (set) of the directory names from the list of all image files
    files = cc.use_server.get_list(img_path)
    dirnames = []
    for i in range(len(files)):
        dirnames.append(files[i].split('/')[4])
    listdir = set(dirnames)

    # remove photos that are not in a directory, to get only directories
    realdir = []
    photo_not_in_dir = []
    for ldir in listdir:
        if '.jpg' in ldir:
            photo_not_in_dir.append(ldir)
        else:
            realdir.append(ldir)
    sortedlist = sorted(realdir)

    # go into the sorted list of directories on the image server and return
    # with a dataframe of image metrics
    if os.path.isfile('./Andra_data.pkl') is False:
        df = cc.read_directory(dirName, sortedlist, files)
        df = df.to_pickle('./Andra_data.pkl')
    else:
        df = pd.read_pickle('./Andra_data.pkl')
    df = df.reset_index(drop=True)

    # add image information csv file next to the calcimetry csv file
    cc.calcimetry.dataframe2csvs(df, dirName)

    # merge the two data sets: calcimetry and image information

    # run the interface to click on images from the directory of
