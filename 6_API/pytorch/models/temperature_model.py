# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 15:02:01 2018

@author: hyunb
"""

import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models


class res_fashion_CNN(nn.Module):
    def __init__(self):
        super(res_fashion_CNN, self).__init__()
        resnet = models.resnet50(pretrained=True)
        for param in resnet.parameters():
            param.requires_grad_(False)
        
        # Requires the last CNN layer to be trained
        # This requires more computing power
        self.last_children = list(resnet.children())[-3]
        self.last_bottle = list(self.last_children)[-1]
        for param in self.last_bottle.parameters():
            param.requires_grad_(True)
        
        modules = list(resnet.children())[:-1]
        self.resnet = nn.Sequential(*modules)
        self.linear1 = nn.Linear(resnet.fc.in_features, 1024)
        self.linear2 = nn.Linear(1024, 512)
        self.linear3 = nn.Linear(512, 256)
        self.linear4 = nn.Linear(256, 1)
        self.bn1 = nn.BatchNorm1d(1024)
        self.bn2 = nn.BatchNorm1d(512)
        self.bn3 = nn.BatchNorm1d(256)
        self.drop = nn.Dropout2d(p=0.1)

    def forward(self, images):
        output = self.resnet(images)
        output = output.view(output.size(0), -1)
        output = self.drop(F.relu(self.linear1(output)))
        output = self.bn1(output)
        output = self.drop(F.relu(self.linear2(output)))
        output = self.bn2(output)
        output = self.drop(F.relu(self.linear3(output)))
        output = self.bn3(output)
        output = self.linear4(output)
        return output