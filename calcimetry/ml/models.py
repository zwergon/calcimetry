import os.path

from torchvision import models
import re
import torch
import torch.nn as nn
from clearml import Task


def load_pretrained_model(model, pretrained_filename):

    # '.'s are no longer allowed in module names, but previous _DenseLayer
    # has keys 'norm.1', 'relu.1', 'conv.1', 'norm.2', 'relu.2', 'conv.2'.
    # They are also in the checkpoints in model_urls. This pattern is used
    # to find such keys.
    pattern = re.compile(
        r"^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$"
    )

    model_path = os.path.dirname(pretrained_filename)
    file_name = os.path.basename(pretrained_filename)

    state_dict = torch.hub.load_state_dict_from_url('http://dummy', model_dir=model_path, file_name=file_name)
    for key in list(state_dict.keys()):
        res = pattern.match(key)
        if res:
            new_key = res.group(1) + res.group(2)
            state_dict[new_key] = state_dict[key]
            del state_dict[key]
    model.load_state_dict(state_dict)

def create_model(name):
    if name == "resnet18":
        model = models.resnet18(pretrained=False)
    elif name == "densenet169":
        model = models.densenet169(pretrained=False)
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


def get_model(name, dropout=0.9, pretrained_filename=None, device=None):

    model = create_model(name)
    if pretrained_filename is not None:
        load_pretrained_model(model, pretrained_filename)

    add_regression_layer(name, model, dropout)

    if device is not None:
        model = model.to(device)

    return model


if __name__ == "__main__":
    model = get_model('resnet18')
    print(model)