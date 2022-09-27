
import numpy as np

class Polyline:

    def __init__(self, pts):
        self.empty = len(pts) == 0
      
        self.x = np.zeros(len(pts))
        self.y = np.zeros(len(pts))
        for i, pt in enumerate(pts):
            self.x[i] = pt[0]
            self.y[i] = pt[1] 

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        if self.current < self.x.shape[0]:
            x, y = self.x[self.current], self.y[self.current]
            self.current += 1
            return x, y
        else:
            raise StopIteration

    @property
    def mean(self):
        if not self.empty:
            return int(np.mean(self.y))
        return 0


    def p_y(self, x):
        if x < np.min(self.x) or x > np.max(self.x):
            return self.mean
        i = 0
        while self.x[i] < x:
            i += 1
        if i == 0:
            return self.y[i]
        ratio = (x - self.x[i-1]) / (self.x[i] - self.x[i-1])

        return self.y[i-1] + ratio*(self.y[i]-self.y[i-1])