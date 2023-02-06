import os.path

from torchvision import models
from torchvision.models import ResNet18_Weights, DenseNet169_Weights
import re
import torch
import torch.nn as nn
from clearml import Task


def load_weights(name):

    if name == "resnet18":
        weights = ResNet18_Weights.DEFAULT
    elif name == "densenet169":
        weights = DenseNet169_Weights.DEFAULT
    else:
        weights = None

    return weights



def create_model(name, weights=None):
    if name == "resnet18":
        model = models.resnet18(weights=weights)
    elif name == "densenet169":
        model = models.densenet169(weights=weights)
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

    if pretrained:
        weights = load_weights(name)

    model = create_model(name, weights=weights)
    
    add_regression_layer(name, model, dropout)

    if device is not None:
        model = model.to(device)

    return model


if __name__ == "__main__":
    model = get_model('resnet18')
    print(model)