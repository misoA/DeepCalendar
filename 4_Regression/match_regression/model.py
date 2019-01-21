# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 15:02:01 2018

@author: hyunb
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

import configure as cf

class res_fashion_CNN(nn.Module):
    def __init__(self):
        super(res_fashion_CNN, self).__init__()
        
        resnet_1 = models.resnet50(pretrained=True)
        resnet_2 = models.resnet50(pretrained=True)
        
        for param in resnet_1.parameters():
            param.requires_grad_(False)
        
        for param in resnet_2.parameters():
            param.requires_grad_(False)

        # Requires the last CNN layer to be trained
        # This requires more computing power
        self.last_children_1 = list(resnet_1.children())[-3]
        self.last_bottle_1 = list(self.last_children_1)[-1]
        for param in self.last_bottle_1.parameters():
            param.requires_grad_(True)
        
        self.last_children_2 = list(resnet_2.children())[-3]
        self.last_bottle_2 = list(self.last_children_2)[-1]
        for param in self.last_bottle_2.parameters():
            param.requires_grad_(True)

        modules_1 = list(resnet_1.children())[:-1]
        self.resnet_1 = nn.Sequential(*modules_1)
    
        modules_2 = list(resnet_2.children())[:-1]
        self.resnet_2 = nn.Sequential(*modules_2)

        self.linear1 = nn.Linear(resnet_1.fc.in_features * 2, 1024)
        self.linear2 = nn.Linear(1024, 512)
        self.linear3 = nn.Linear(512, 256)
        self.linear4 = nn.Linear(256, 1)
        self.bn1 = nn.BatchNorm1d(1024)
        self.bn2 = nn.BatchNorm1d(512)
        self.bn3 = nn.BatchNorm1d(256)
        self.drop = nn.Dropout2d(p=0.1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, images):
        output_1 = self.resnet_1(images[0])
        output_2 = self.resnet_2(images[1])

        output_1 = output_1.view(output_1.size(0), -1)
        output_2 = output_2.view(output_2.size(0), -1)
        
        # TODO - Put the code at this part to concatenate two outputs
        # (batch size, resnet.fc.in_features)
        # -> (batch size, resnet.fc.in_features * 2)
        output = torch.cat([output_1, output_2], dim=1)
    
        output = self.drop(F.relu(self.linear1(output)))
        output = self.bn1(output)
        output = self.drop(F.relu(self.linear2(output)))
        output = self.bn2(output)
        output = self.drop(F.relu(self.linear3(output)))
        output = self.bn3(output)
        output = self.linear4(output)
        output = self.sigmoid(output)
    
        return output