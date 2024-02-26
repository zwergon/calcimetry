

class Normalize:

    def __call__(self, x):
        return x/100.
    
    def inv(self, x):
        return x*100