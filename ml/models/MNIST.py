from typing import Type

import torch
import torch.nn as nn
import torch.nn.functional as F

from ml.datasets.MNIST import MNISTDataset
from ml.datasets.dataset import Dataset
from ml.models.model import Model


class MNIST(Model):
    """
    This model has been adapted from https://arxiv.org/abs/2008.10400 (M5), which is currently the best performing model
    on the MNIST dataset (99.91%), according to https://paperswithcode.com/sota/image-classification-on-mnist.
    We use the second version proposed in this paper (M5), which has an accuracy of 99.80%.
    """

    def get_dataset_class(self) -> Type[Dataset]:
        return MNISTDataset

    def __init__(self):
        super(MNIST, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 5, bias=False)
        self.conv1_bn = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 5, bias=False)
        self.conv2_bn = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 96, 5, bias=False)
        self.conv3_bn = nn.BatchNorm2d(96)
        self.conv4 = nn.Conv2d(96, 128, 5, bias=False)
        self.conv4_bn = nn.BatchNorm2d(128)
        self.conv5 = nn.Conv2d(128, 160, 5, bias=False)
        self.conv5_bn = nn.BatchNorm2d(160)
        self.fc1 = nn.Linear(10240, 10, bias=False)

    def get_logits(self, x):
        x = (x - 0.5) * 2.0
        conv1 = F.relu(self.conv1_bn(self.conv1(x)))
        conv2 = F.relu(self.conv2_bn(self.conv2(conv1)))
        conv3 = F.relu(self.conv3_bn(self.conv3(conv2)))
        conv4 = F.relu(self.conv4_bn(self.conv4(conv3)))
        conv5 = F.relu(self.conv5_bn(self.conv5(conv4)))
        flat5 = torch.flatten(conv5.permute(0, 2, 3, 1), 1)
        return self.fc1(flat5)

    def forward(self, x):
        logits = self.get_logits(x)
        return F.log_softmax(logits, dim=1)
