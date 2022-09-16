

class Measurement:

    def __init__(self, measure_id, cote, val_1m, val_15m) -> None:
        self.measure_id = measure_id
        self.cote = cote
        self.val_1m = val_1m
        self.val_15m = val_15m


    def __repr__(self) -> str:
        return f"Measure ({self.measure_id}): ({self.cote}->{self.val_1m})"