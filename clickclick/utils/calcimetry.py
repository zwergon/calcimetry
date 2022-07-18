"""
A library of python functions for extracting the Andra metadata, data and
images
"""

import cv2
import torch
import piq
import os.path
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from collections import Counter

# local library of functions to connect to image server
import utils.use_server as server


def variance_of_laplacian(image):
    """
    compute the Laplacian of the image and then return the focus
    measure, which is simply the variance of the Laplacian
    :param image:
    :return:
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()


def gradient_magnitude(image):
    """
    Get magnitude of gradient for given image
    :param image:
    :return:
    """
    ddepth = cv2.CV_64F
    dx = cv2.Sobel(image, ddepth, 1, 0)
    dy = cv2.Sobel(image, ddepth, 0, 1)
    mag = cv2.magnitude(dx, dy)
    return mag


def prep_image(raw_img):
    """
    Function to prepare an image for colour analysis
    :param raw_img:
    :return:
    """
    modified_img = cv2.resize(raw_img, (900, 600),
                              interpolation=cv2.INTER_AREA)
    modified_img = modified_img.reshape(modified_img.shape[0]
                                        * modified_img.shape[1], 3)
    return modified_img


def color_analysis(img):
    """
    Function to perform cluster analysis to group the 5 top colours within
    the image
    :param img:
    :return:
    """
    clf = KMeans(n_clusters=5)  # 5 top colours
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    return ordered_colors


def read_directory(filelocs, fileloc, allfiles, quiet=True):
    """
    Function to read all images in a directory and return a data frame with
    image metrics
    :param filelocs: Name of directory where excell files are
    :param fileloc: Name of directory of images to be read
    :param allfiles: List of all files in the image server
    :param quiet: no http messages
    :return df: Pandas dataframe of image metrics
    """
    ImageId = []
    Path = []
    FileName = []
    DrillName = []
    Cote0 = []
    Cote1 = []
    PxSize = []
    PySize = []
    Focus = []
    GradientMax = []
    GradientSTD = []
    Colour1 = []
    Colour2 = []
    Colour3 = []
    Colour4 = []
    Colour5 = []
    BRISQUE_i = []
    BRISQUE_l = []

    for file in allfiles:
        if fileloc in file:
            img = server.get_file(file, quiet)

            # if img.size() > 89478485:
            #    continue
            l0 = file.split('/')[-1]
            l1 = l0.split('.')[0]
            l2 = l1.split('_')
            if len(l2) < 3:
                continue
            width, height = img.size
            if width * height > 89478485:
                print(f'Not enough memory to process image {file}'
                      f' with PyTorch on local ')
            ImageId.append(0)
            Path.append(file)
            FileName.append(l0)
            DrillName.append(l2[-3])
            Cote0.append(l2[-2])
            Cote1.append(l2[-1])
            PxSize.append(width)
            PySize.append(height)

            # focus metric
            gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
            Focus.append(variance_of_laplacian(gray))

            # Gradient metric
            GradientMax.append(np.max(gradient_magnitude(gray)[:]))
            GradientSTD.append(np.std(gradient_magnitude(gray)[:]))

            # Top five colours
            try:
                colours = color_analysis(prep_image(np.asarray(img)))
                Colour1.append(colours[0])
                Colour2.append(colours[1])
                Colour3.append(colours[2])
                Colour4.append(colours[3])
                Colour5.append(colours[4])
            except Exception as e:
                print(e)
                Colour1.append(np.nan)
                Colour2.append(np.nan)
                Colour3.append(np.nan)
                Colour4.append(np.nan)
                Colour5.append(np.nan)

            # pytorch image quality, use try, except loop to kep going if image
            # is too large or does not conform
            try:
                x = torch.tensor(np.asarray(img)).permute(2, 0, 1)[
                        None, ...] / 255.
                if torch.cuda.is_available():
                    # Move to GPU to make computaions faster
                    # print(torch.cuda.is_available())
                    x = x.cuda()
                brisque_index: torch.Tensor = piq.brisque(x, data_range=1.,
                                                          reduction='none')
                brisque_loss: torch.Tensor = piq.BRISQUELoss(data_range=1.,
                                                             reduction='none')(
                    x)

                BRISQUE_i.append(brisque_index.item())
                BRISQUE_l.append(brisque_loss.item())
            except Exception as e:
                print(f'Error in PyTorch with image {file}\n' + e)
                BRISQUE_i.append(np.nan)
                BRISQUE_l.append(np.nan)

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            del x

    d = {'ImageId': ImageId, 'Path': Path, 'FileName': FileName,
         'DrillName': DrillName,
         'Cote0': Cote0, 'Cote1': Cote1, 'PxSize': PxSize, 'PySize': PySize,
         'Focus': Focus,
         'Gradient max': GradientMax, 'Gradient std': GradientSTD,
         'Colour1': Colour1, 'Colour2': Colour2, 'Colour3': Colour3,
         'Colour4': Colour4, 'Colour5': Colour5, 'BRISQUE index': BRISQUE_i,
         'BRISQUE loss': BRISQUE_l}
    df = pd.DataFrame(data=d)

    return df


def dataframe2csvs(df, filelocs):
    """
    Function to keep output to individual csv files per drill name
    :param df: global dataframe
    :param filelocs: location of Excell files
    :return:
    """
    DrillLocations = set(list(df['DrillName']))
    for i, location in enumerate(DrillLocations):
        path_to_output = '{}{}'.format(filelocs, location)
        dfl = df.loc[df['DrillName'].isin([location])]
        if os.path.exists(path_to_output):
            csv_file = '{}/image-info.csv'.format(path_to_output, location)
            print(csv_file)
            dfl.to_csv(csv_file)
        else:
            print(f'{path_to_output} does not exist')


def excell2csv(filelocs):
    """
    function to go through the directories of calcimetry spread
    :param filelocs: location of the files/directories
    :return:
    """
    directories = []
    for name in os.listdir(filelocs):
        if os.path.isdir(filelocs + name):
            directories.append(filelocs + name)

    excell_files = []
    for directory in directories:
        for fname in os.listdir(directory):
            if os.path.isfile(f'{directory}/{fname}'):
                if '.xls' in fname:
                    # different file names of course
                    if 'Calcimétrie' in fname and 'Zone.Identifier' not in fname:
                        excell_files.append(f'{directory}/{fname}')
                    elif 'CALCIMETRIE' in fname and 'Zone.Identifier' not in fname:
                        excell_files.append(f'{directory}/{fname}')
                    elif 'Calcimètre' in fname and 'Zone.Identifier' not in fname:
                        excell_files.append(f'{directory}/{fname}')
                    elif 'Calci' in fname and 'Zone.Identifier' not in fname:
                        excell_files.append(f'{directory}/{fname}')
                    elif 'calcimétrie' in fname and 'Zone.Identifier' not in fname:
                        excell_files.append(f'{directory}/{fname}')

    dfcolms = []
    for file in excell_files:
        print(file)
        df = pd.read_excel(file)
        sf = df.iloc[:, 0]
        if 'Cote' in list(sf) or 'Cote (m)' in list(sf):
            dfcolms.append(len(df.columns))

            if len(df.columns) < 5:
                print(file)
                break

            if len(df.columns) > 7:
                for i in range(7, len(df.columns)):
                    colname = f'Unnamed: {i}'
                    df = df.drop([colname], axis=1)

            dfe = df.dropna().copy()
            dfe.columns = ['Cote', 'à 1 minute', 'à 4 minutes', 'à 19 minutes',
                           '% CaCO3', '% Dolomie', '% insolubles']

        elif 'Cote toit' in list(sf):
            dfcolms.append(len(df.columns))

            if len(df.columns) < 5:
                print(file)
                break

            if len(df.columns) > 7:
                for i in range(7, len(df.columns)):
                    colname = f'Unnamed: {i}'
                    df = df.drop([colname], axis=1)

            dfe = df.dropna().copy()
            dfe.drop(df.columns[1], axis=1)
            dfe.columns = ['Cote', 'à 1 minute', 'à 3 minutes', 'à 15 minutes',
                           '% CaCO3', '% Dolomie', '% insolubles']

        else:
            dfe = pd.DataFrame(columns=['Cote', 'à 1 minute', 'à 3 minutes',
                                        'à 15 minutes', '% CaCO3', '% Dolomie', '% insolubles'])

        csv_file = file.split('.xls')[0] + '.csv'
        print(csv_file)
        dfe.to_csv(csv_file)
        del dfe
        del df
