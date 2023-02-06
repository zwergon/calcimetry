import numpy as np

from calcimetry.mongo_api import MongoInfo
from calcimetry.thumbnail_api import ThumbnailAPI

from calcimetry.ml.dataset import CalciDataset

__all__ = [
    "generate_datasets"
]

def generate_datasets(host="localhost", port=27010, train_val_ratio=.8):

    mongo_info = MongoInfo(host, port)
    with ThumbnailAPI(mongo_info=mongo_info) as thumb_api:
        n_total = thumb_api.size()
        indices = np.arange(n_total)
        #np.random.shuffle(indices)
        n_train = train_val_ratio *  n_total

        trains = []
        valids = []
        
        for i in range(n_total):
            idx = int(indices[i])
            thumb = thumb_api.read(idx)
            array = np.asarray(thumb.jpg.convert('RGB'))
            if i < n_train:
                trains.append( (array, thumb.measurement.val_1m) )
            else:
                valids.append( (array, thumb.measurement.val_1m) )

    return CalciDataset(trains), CalciDataset(valids)

    