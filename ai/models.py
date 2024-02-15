
from typing import Callable, List, Optional, Type, Union
from torch.nn.modules import Module
from torchvision.models.resnet import BasicBlock, Bottleneck, ResNet

class CalciResnet(ResNet):

    def __init__(self, loader, config) -> None:
        super().__init__(BasicBlock, [2, 2, 2, 2], num_classes=1)