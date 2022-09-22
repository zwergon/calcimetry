"""
quality
=======
class for various quality measurements
"""

import cv2
import piq
import torch
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

from calcimetry.mongo_api import MongoAPI, MongoInfo

class Quality:

    def __init__(self, image_id, focus=None, gradient=None, colours=None,
                 brisque=None):
        self.ImageId = image_id
        if focus is None:
            self.focus = -1
        else:
            self.focus = focus
        if gradient is None:
            self.gradient = {'min': -1,
                             'max': -1,
                             'ave': -1,
                             'std': -1}
        else:
            self.gradient = gradient
        if colours is None:
            self.colours =  []
        else:
            self.colours = colours
        if brisque is None:
            self.brisque = -1
        else:
            self.brisque = brisque

    @staticmethod
    def variance_of_laplacian(image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(image, cv2.CV_64F).var()

    @staticmethod
    def gradient_magnitude(image):
        # Get magnitude of gradient for given image
        ddepth = cv2.CV_64F
        dx = cv2.Sobel(image, ddepth, 1, 0)
        dy = cv2.Sobel(image, ddepth, 0, 1)
        mag = cv2.magnitude(dx, dy)
        return mag

    @staticmethod
    def prep_image(image):
        # Reduce image for colour clustering
        modified_img = cv2.resize(image, (900, 600),
                                  interpolation=cv2.INTER_AREA)
        modified_img = modified_img.reshape(modified_img.shape[0]
                                            * modified_img.shape[1], 3)
        return modified_img

    @staticmethod
    def color_analysis(image, n_clusters):
        # Calculate top 5 colours using KMeans clustering analysis
        clf = KMeans(n_clusters=n_clusters)  # top colours
        color_labels = clf.fit_predict(image)
        center_colors = clf.cluster_centers_
        counts = Counter(color_labels)
        ordered_colors = [center_colors[i].tolist() for i in counts.keys()]
        return ordered_colors

    @staticmethod
    def brisque_index(image, max_image_size=89478485):
        x = torch.tensor(np.asarray(image)).permute(2, 0, 1)[
                None, ...] / 255.
        gpu_used = False
        width, height = image.size
        image_size = width * height
        if torch.cuda.is_available() and image_size < max_image_size:
            # Move to GPU to make computaions faster
            # print(torch.cuda.is_available())
            x = x.cuda()
            gpu_used = True
        brisque_index: torch.Tensor = piq.brisque(x, data_range=1.,
                                                  reduction='none')
        if gpu_used is True:
            torch.cuda.empty_cache()
        del x
        return brisque_index.item()

    def add_simple_metrics(self, image):
        """
        Add the simple metrics of an image: Converts the image to a gray
        scale and then calculates the variance of the laplacian of the gray
        scale image

        :param image: image read in from CalcimetryAPI.read_image
        """

        gray = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2GRAY)
        self.focus = self.variance_of_laplacian(gray)
        self.gradient['min'] = np.min(self.gradient_magnitude(gray)[:])
        self.gradient['max'] = np.max(self.gradient_magnitude(gray)[:])
        self.gradient['ave'] = np.mean(self.gradient_magnitude(gray)[:])
        self.gradient['std'] = np.std(self.gradient_magnitude(gray)[:])

    def add_colours(self, image, n_clusters):
        """
        Add the 5 most common colours using KMeans clustering

        :param image: image file
        :param: n_clusters: number of top colours to rank, e.g. top 3, or top 5
        """
        self.colours.append(self.color_analysis(self.prep_image(np.asarray(
            image)), n_clusters))

    def add_brisque_index(self, image, max_image_size=89478485):
        """
        Add the BRISQUE index (using the piq libary)
        doi: 10.1109/TIP.2012.2214050

        :param image: image file
        :param: max_image_size: maximum image size below wich the GPU is
        used to calculate the BRISQUE index.
        :return:
        """

        self.brisque = self.brisque_index(image, max_image_size)
