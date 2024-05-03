import random

from inferator import Inferfator


def compute_calcimetry(image: str, coords: list):

    calcimetries = []

    inferators = Inferfator.create_inferators(image, coords)
    calcimetries.append(("position", [x for x, y in coords]))
    for infe in inferators:
        infe.compute()
        calcimetries.append((infe.name, infe.calcimetries))

    return calcimetries
