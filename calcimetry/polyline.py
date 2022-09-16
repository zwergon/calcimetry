
import numpy as np

class Polyline:

    def __init__(self, pts) -> None:
        self.cotes = np.zeros(len(pts))
        self.y = np.zeros(len(pts))
        for i, pt in enumerate(pts):
            self.cotes[i] = pt[0]
            self.y[i] = pt[1] 

    @property
    def mean(self):
        return np.mean(self.y)


    def p_y(self, cote):
        if cote < np.min(self.cotes) or cote > np.max(self.cotes):
            raise IndexError("cote en dehors")
        i = 0
        while self.cotes[i] < cote:
            i += 1
        if i == 0:
            return self.y[i]
        ratio = (cote - self.cotes[i-1]) / (self.cotes[i] - self.cotes[i-1])

        return self.y[i-1] + ratio*(self.y[i]-self.y[i-1])