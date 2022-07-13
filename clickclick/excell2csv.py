"""
Go through all the directories and make individual csv files from the excell
ones
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