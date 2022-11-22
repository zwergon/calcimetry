

class Measurement:

    def __init__(self, image_id, measure_id, cote, val_1m, val_15m, quality):
        self.image_id = image_id
        self.measure_id = measure_id
        self.cote = cote
        self.val_1m = val_1m
        self.val_15m = val_15m
        self.quality = quality

    @classmethod
    def from_dict(cls, m_dict):
        return cls(
            m_dict['image_id'], 
            m_dict['measurement_id'], 
            m_dict['cote'], 
            m_dict['val_1m'], 
            m_dict['val_15m'],
            m_dict['quality'])

    def to_dict(self):
        return {
            "image_id": self.image_id,
            "measurement_id": self.measure_id,
            "cote": self.cote,
            "val_1m": self.val_1m,
            "val_15m": self.val_15m,
            "quality": self.quality
        }

    def __repr__(self):
        return f"Measure: #{self.measure_id} (image {self.image_id}): ({self.cote}->{self.val_1m}) quality:{self.quality}"