

class CarrotImage:

    def __init__(self, jpg, resolution = 1., w_transform = (0, 1)) -> None:
        self.jpg = jpg
        self.resolution = resolution
        self.w_transform = w_transform

    def to_world(self, px):
        return self.w_transform[0] + self.w_transform[1]*px
       
    def to_pixel(self, wx):
        return (wx - self.w_transform[0]) / self.w_transform[1]

    def vignette(self, dim=128, center = None, resolution=None):
        if resolution is not None:
            img = self.to_resolution(self.jpg)
        else:
            img = self.jpg

        if center is None:
            w, h = img.size
            cx, cy = w // 2, h //2
        else:
            cx, cy = center[0], center[1]

        half_dim = dim // 2
        left = cx - half_dim
        top = cy - half_dim
        right =  cx + half_dim
        bottom = cy + half_dim

        vignette = img.crop( (left, top, right, bottom))
        return vignette

    def to_resolution(self, resolution):
        return self.jpg