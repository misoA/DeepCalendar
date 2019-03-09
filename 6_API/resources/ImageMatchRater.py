# -*- coding: utf-8 -*-
import os, sys
from collections import OrderedDict
import numpy as np

sys.path.append("..")

from flask_restful import Resource
from flask import request
from resources.S3Image import get_image_from_s3
import urllib.request as urlRequest

class RatingMatchImage(Resource):
    def get(self):
        imTopName = request.args.get('imTopName')
        imBottomName = request.args.get('imBottomName')
        imTopCode = request.args.get('imTopCode')
        imBottomCode = request.args.get('imBottomCode')
            
        if imTopCode == 'RE_1':
            urlRequest.urlretrieve(imTopName, os.path.join(img_folder, 'top_image.jpg'))
        else:
            get_image_from_s3(imTopName, os.path.join(img_folder, 'top_image.jpg'))
            
        if imBottomCode == 'RE_1':
            urlRequest.urlretrieve(imBottomName, os.path.join(img_folder, 'bottom_image.jpg'))
        else:
            get_image_from_s3(imBottomName, os.path.join(img_folder, 'bottom_image.jpg'))
        returnString = analysis_match(img_folder, match_list_gen(img_folder))
        return returnString['match_0']['match']
    
    def post(self):
        imTopName = request.args.get('imTopName')
        imBottomName = request.args.get('imBottomName')
        imTopCode = request.args.get('imTopCode')
        imBottomCode = request.args.get('imBottomCode')
        
        if imTopCode == 'RE_1':
            urlRequest.urlretrieve(imTopName, os.path.join(img_folder, 'top_image.jpg'))
        else:
            get_image_from_s3(imTopName, os.path.join(img_folder, 'top_image.jpg'))
            
        if imBottomCode == 'RE_1':
            urlRequest.urlretrieve(imBottomName, os.path.join(img_folder, 'bottom_image.jpg'))
        else:
            get_image_from_s3(imBottomName, os.path.join(img_folder, 'bottom_image.jpg'))
        returnString = analysis_match(img_folder, match_list_gen(img_folder))
        return returnString['match_0']['match']


from pytorch import configure as cf
from pytorch.models.match_model import res_fashion_CNN as match_CNN
from pytorch.data_loader import get_loader_match

import torch
from torchvision import transforms


transform = transforms.Compose([ 
    transforms.Resize(224),                          # smaller edge of image resized to 256
    transforms.RandomCrop(224),                      # get 224x224 crop from random location
#    transforms.RandomHorizontalFlip(),               # horizontally flip image with probability=0.5
    transforms.ToTensor(),                           # convert the PIL Image to a tensor
    transforms.Normalize((0.485, 0.456, 0.406),      # normalize image for pre-trained model
                         (0.229, 0.224, 0.225))])
# Configure file
url = cf.url

#image folder
img_folder = 'PUT_YOUR_PATH'
#pkl folder
pkl_folder = 'PUT_YOUR_PATH'

# cuda available
dv = "cuda" if torch.cuda.is_available() else 'cpu'

batch_size = 1

device = torch.device(dv)
match_cnn = match_CNN()
match_file = 'match.pkl'
match_cnn.load_state_dict(torch.load(os.path.join(pkl_folder, match_file),
                                       map_location=dv))
match_cnn.eval()
match_cnn.to(device)


def match_list_gen(match_folder):
    img_list = os.listdir(match_folder)
    img_len = len(img_list)
    assert img_len % 2 == 0, "Please set the match image set to even QUARK!"
    
    match_list = []
    for i in range(int(img_len / 2)):
        img_1_id = i * 2
        img_2_id = img_1_id + 1
        match_list.append((img_list[img_1_id], img_list[img_2_id]))

    return match_list

def torch_to_list(torch_output):
    num_list = []
    torch_data = torch_output.data[0]
    for i in range(len(torch_data)):
        num_list.append(torch_data[i].item())
    num_list = np.array(num_list)
    return num_list

def match_analysis(image_1, image_2, url_1, url_2):
    # Initialize the result
    match_result = OrderedDict()
    match_output = match_cnn((image_1, image_2))
    match = torch_to_list(match_output)
    match = round(match[0] * 100, 4)
    match_result['image_1'] = url_1
    match_result['image_2'] = url_2
    match_result['match'] = match
    
    return match_result

def analysis_match(match_folder, match_file):
    print("Using device :", dv)
    analysis = OrderedDict()
    data_loader = get_loader_match(transform=transform,
                         mode='test',
                         batch_size=batch_size,
                         img_folder=match_folder,
                         image_file=match_file)
    
    for batch_i, image in enumerate(data_loader):
        print("Processing...", batch_i)
        image_1 = image[0].to(device)
        image_2 = image[1].to(device)
        json_result = match_analysis(image_1,
                                     image_2,
                                     match_file[batch_i][0],
                                     match_file[batch_i][1])
        analysis['match_{}'.format(batch_i)] = json_result
    
    return analysis
    