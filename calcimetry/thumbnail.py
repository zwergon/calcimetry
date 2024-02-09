
from calcimetry.measurement import Measurement
from PIL import Image
import base64
import io

class Thumbnail:

    def __init__(self, version, jpg: Image, bbox, measurement: Measurement = None ):
        self.version = version
        self.jpg = jpg 
        self.bbox = bbox
        self.measurement = measurement

    @property
    def image_id(self):
        if self.measurement is not None:
            return self.measurement.image_id
        return -1
    
    @property
    def val_1m(self):
        if self.measurement is not None:
            return self.measurement.val_1m
        return -1
        
    @staticmethod
    def to_base64(jpg):
        byte_array = io.BytesIO()
        jpg.save(byte_array, format='jpeg')
        return base64.b64encode(byte_array.getvalue()).decode()

    @staticmethod
    def from_base64(b64):
        byte_array = base64.b64decode(b64.encode())
        im_file = io.BytesIO(byte_array)
        return Image.open(im_file)
     
    @classmethod
    def from_dict(cls, th_dict):
        version = th_dict['version']
        bbox = th_dict['bbox']
        m = Measurement.from_dict(th_dict['measurement'])
        jpg = Thumbnail.from_base64(th_dict['jpg/base64'])
        return cls(version=version, jpg=jpg, bbox=bbox, measurement=m)


    def to_dict(self):
        return {
          "version": self.version,
          "measurement": self.measurement.to_dict(),
          "bbox": self.bbox,
          "jpg/base64": Thumbnail.to_base64(self.jpg)
        }

