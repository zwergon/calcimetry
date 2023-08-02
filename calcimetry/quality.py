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

from PIL import Image
from calcimetry.mongo_api import MongoAPI

class Quality:

    MAX_IMAGE_SIZE=89478485 # maximum image size below wich the GPU is used to calculate the BRISQUE index
    
    @staticmethod
    def _variance_of_laplacian(image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(image, cv2.CV_64F).var()

    @staticmethod
    def _gradient_magnitude(image):
        # Get magnitude of gradient for given image
        ddepth = cv2.CV_64F
        dx = cv2.Sobel(image, ddepth, 1, 0)
        dy = cv2.Sobel(image, ddepth, 0, 1)
        mag = cv2.magnitude(dx, dy)
        return mag

    @staticmethod
    def _prep_image(image):
        # Reduce image for colour clustering
        modified_img = cv2.resize(image, (900, 600),
                                  interpolation=cv2.INTER_AREA)
        modified_img = modified_img.reshape(modified_img.shape[0]
                                            * modified_img.shape[1], 3)
        return modified_img
     
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

    @staticmethod
    def color_analysis(image, n_clusters):
        # Calculate top 5 colours using KMeans clustering analysis
        clf = KMeans(n_clusters=n_clusters)  # top colours
        color_labels = clf.fit_predict(image)
        center_colors = clf.cluster_centers_
        counts = Counter(color_labels)
        ordered_colors = [center_colors[i].tolist() for i in counts.keys()]
        return ordered_colors

    def __init__(self, image: Image, n_clusters=3):
        self.image = image
        self.focus = -1
        self.gradient = {'min': -1,
                            'max': -1,
                            'ave': -1,
                            'std': -1}
        self.n_clusters = n_clusters
        self.colours =  []
        self.brisque = -1
        
    def _compute_simple_metrics(self):
        """
        Add the simple metrics of an image: Converts the image to a gray
        scale and then calculates the variance of the laplacian of the gray
        scale image
        """

        gray = cv2.cvtColor(np.asarray(self.image), cv2.COLOR_BGR2GRAY)
        self.focus = Quality._variance_of_laplacian(gray)
        self.gradient['min'] = np.min(self._gradient_magnitude(gray)[:])
        self.gradient['max'] = np.max(self._gradient_magnitude(gray)[:])
        self.gradient['ave'] = np.mean(self._gradient_magnitude(gray)[:])
        self.gradient['std'] = np.std(self._gradient_magnitude(gray)[:])

    def _compute_colors(self):
        """
        Add the self.n_cluters most common colours using KMeans clustering
        """
        self.colours= self.color_analysis(
                Quality._prep_image(np.asarray(self.image)), 
                self.n_clusters
                )
            

    def _compute_brisque_index(self):
        """
        computes the BRISQUE index (using the piq libary)
        doi: 10.1109/TIP.2012.2214050

        """

        self.brisque = self.brisque_index(self.image, Quality.MAX_IMAGE_SIZE)


    def compute(self):
        self._compute_simple_metrics()
        self._compute_colors()
        self._compute_brisque_index()

    def to_dict(self):
        return {
            "focus": self.focus,
            "gradient": self.gradient,
            "colours": self.colours,
            "brisque": self.brisque
        }

    @classmethod
    def from_dict(cls, q_dict):
        quality = cls(None)
        quality.focus = q_dict['focus']
        quality.gradient = q_dict['gradient']
        quality.colours = q_dict['colours']
        quality.brisque = q_dict['brisque']
        return quality

    def __repr__(self) -> str:
        str = "Quality\n"
        str += f".focus: {self.focus}\n"
        str += f".gradient: {self.gradient}\n"
        str += f".colours: {self.colours}\n"
        str += f".brisque: {self.brisque}"
        return str