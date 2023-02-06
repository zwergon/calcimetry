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

    if name == "resnet18":
        weights = load_state_dict_from_url(url="http://dummy", 
                                           file_name= os.path.join(model_path, "resnet18-f37072fd.pth")) 
    elif name == "densenet169":
        weights = load_state_dict_from_url(url="http://dummy", 
                                           file_name=  os.path.join(model_path, "densenet169-b2777c0a.pth"))
    else:
        weights = None

    return weights

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


def get_model(name, dropout=0.9, pretrained=True, device=None):

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