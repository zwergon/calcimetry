from PIL import Image

Image.MAX_IMAGE_PIXELS = 933120000

class CarrotImage:

    def __init__(self, jpg: Image, infos: dict, measurements = []) -> None:
        self.infos = {
            "image_id": -1,
            "w_extent": (0, 1), # default value
            "resolution": 1., # default value
            "k_arrow": None, # a Polyline object at the middle of the carrot
            "k_up": None,
            "k_down": None,
            "measurements": measurements
        }
        self.jpg = jpg
        self.infos['px_extent'] = self.jpg.size if jpg is not None else 1 # default value
        self.infos.update(infos)

    @property
    def image_id(self):
        return self.infos['image_id']

    @property
    def resolution(self):
        px_extent = self.infos['px_extent']
        w_extent = self.infos['w_extent']
        return abs((w_extent[1]-w_extent[0])/(px_extent[1]-px_extent[0]))

    @property
    def y_ratio(self):
        y_up_mean = self.k_up.mean
        
        y_down_mean = self.k_down.mean
        _, h = self.jpg.size
        return (y_down_mean-y_up_mean)/h # y scale reverse y_down > y_up

    @property
    def k_arrow(self):
        return self.infos['k_arrow']

    @property
    def k_up(self):
        return self.infos['k_up']

    @property
    def k_down(self):
        return self.infos['k_down']

    @property
    def measurements(self):
        return self.infos['measurements']
    
    @property
    def n_measurements(self):
        return len(self.infos['measurements'])

    def to_world(self, px):
        px_extent = self.infos['px_extent']
        w_extent = self.infos['w_extent']
        return w_extent[0] + (px-px_extent[0])*(w_extent[1]-w_extent[0])/(px_extent[1]-px_extent[0])
       
    def p_x(self, wx):
        px_extent = self.infos['px_extent']
        w_extent = self.infos['w_extent']
        return round(px_extent[0] + (wx-w_extent[0])*(px_extent[1]-px_extent[0])/(w_extent[1]-w_extent[0]))

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
