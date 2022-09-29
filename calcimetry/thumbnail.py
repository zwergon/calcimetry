
from calcimetry.quality import Quality
from calcimetry.measurement import Measurement
from PIL import Image
import base64
import io

class Thumbnail:

    def __init__(self, thu_id, jpg: Image, quality: Quality = None, measurement: Measurement = None ):
        self.thu_id = thu_id
        self.jpg = jpg 
        self.measurement = measurement
        if quality is None:
            self.quality = Quality(jpg)
            self.quality.compute()
        else:
            self.quality = quality

    @property
    def image_id(self):
        if self.measurement is not None:
            return self.measurement.image_id
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
        thu_id = th_dict['ThuId']
        if 'measurement' in th_dict:
            m = th_dict['measurement']
        else:
            m = None
        jpg = Thumbnail.from_base64(th_dict['jpg/base64'])
        return cls(thu_id, jpg, quality=Quality.from_dict(th_dict['quality']), measurement=m)


    def to_dict(self):
        measure_id =  self.measurement.measure_id if self.measurement.measure_id is not None else -1
        return {
          "ThuId": self.thu_id,
          "quality": self.quality.to_dict(),
          "measurement": measure_id,
          "jpg/base64": Thumbnail.to_base64(self.jpg)
        }

