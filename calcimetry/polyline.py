
import numpy as np

class Polyline:

    def __init__(self, pts) -> None:
        self.x = np.zeros(len(pts))
        self.y = np.zeros(len(pts))
        for i, pt in enumerate(pts):
            self.x[i] = pt[0]
            self.y[i] = pt[1] 

    @property
    def mean(self):
        return np.mean(self.y)


    def value(self, cote):
        if cote < np.min(self.x) or cote > np.max(self.x):
            raise IndexError("cote en dehors")
        i = 0
        while self.x[i] < cote:
            i += 1
        if i == 0:
            return self.y[i]
        ratio = (cote - self.x[i-1]) / (self.x[i] - self.x[i-1])

        return self.y[i-1] + ratio*(self.y[i]-self.y[i-1])