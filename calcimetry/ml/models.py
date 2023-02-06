import os.path

import re
import torch
import torch.nn as nn
from clearml import Dataset
from functools import partial

from torchvision import models
from torchvision.models._api import Weights
from torchvision._internally_replaced_utils import load_state_dict_from_url
from torchvision.transforms._presets import ImageClassification


def load_weights(name):

    model_path = Dataset.get(
        dataset_name="Andras",
        dataset_project="models"
    ).get_local_copy()

     # '.'s are no longer allowed in module names, but previous _DenseLayer
    # has keys 'norm.1', 'relu.1', 'conv.1', 'norm.2', 'relu.2', 'conv.2'.
    # They are also in the checkpoints in model_urls. This pattern is used
    # to find such keys.
    pattern = re.compile(
        r"^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$"
    )

    if name == "resnet18":
        state_dict = load_state_dict_from_url(url="http://dummy", 
                                           file_name= os.path.join(model_path, "resnet18-f37072fd.pth")) 
    elif name == "densenet169":
        state_dict = load_state_dict_from_url(url="http://dummy", 
                                           file_name=  os.path.join(model_path, "densenet169-b2777c0a.pth"))
    else:
        state_dict = None

    for key in list(state_dict.keys()):
        res = pattern.match(key)
        if res:
            new_key = res.group(1) + res.group(2)
            state_dict[new_key] = state_dict[key]
            del state_dict[key]

    return state_dict

def create_model(name):
    if name == "resnet18":
        model = models.resnet18(weights=None)
    elif name == "densenet169":
        model = models.densenet169(weights=None)
    else:
        raise Exception(f"model {name} is not useable")

    return model

def add_regression_layer(name, model, dropout):
    if name == "resnet18":
        num_ftrs = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(num_ftrs, 1)
        )
    elif name == "densenet169":
        num_ftrs = model.classifier.in_features
        model.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(num_ftrs, 1)
        )
    else:
        raise Exception(f"model {name} is not useable")


def get_model(config, device=None, pretrained=True):

    name = config['modelname']
    dropout = config['dropout']
    model = create_model(name)

    if pretrained:
        weights = load_weights(name)
        model.load_state_dict(weights)

    add_regression_layer(name, model, dropout)

    if device is not None:
        model = model.to(device)

    return model


if __name__ == "__main__":
    model = get_model('resnet18')
    print(model)