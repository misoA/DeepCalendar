# -*- coding: utf-8 -*-
import os, sys
from collections import OrderedDict
import numpy as np

sys.path.append("..")
from flask_restful import Resource
from flask import request
from resources.S3Image import get_image_from_s3

class ClassificateImage(Resource):
    def get(self):
        imName = request.args.get('imName')
        get_image_from_s3(imName, os.path.join(img_folder, imName))
        returnString = anaylsis(imName)
        return returnString
    
    def post(self):
        imName = request.args.get('imName')
        get_image_from_s3(imName, os.path.join(img_folder, imName))
        returnString = anaylsis(imName)
        return returnString


from pytorch import configure as cf
from pytorch.models.clothes_model import res_fashion_CNN as clothes_CNN
from pytorch.models.schedule_model import res_fashion_CNN as schedule_CNN
from pytorch.models.weather_model import res_fashion_CNN as weather_CNN
from pytorch.models.temperature_model import res_fashion_CNN as temperature_max_CNN
from pytorch.models.temperature_model import res_fashion_CNN as temperature_min_CNN
from pytorch.data_loader import get_loader

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

clothes = cf.clothes
weather = cf.weather
schedule = cf.schedule

batch_size = 1

device = torch.device(dv)

clothes_cnn = clothes_CNN()
schedule_cnn = schedule_CNN()
weather_cnn = weather_CNN()
temperature_max_cnn = temperature_max_CNN()
temperature_min_cnn = temperature_min_CNN()

clothes_file = 'clothes.pkl'
weather_file = 'weather.pkl'
schedule_file = 'schedule.pkl'
temperature_max_file = 'temperature-max.pkl'
temperature_min_file = 'temperature-min.pkl'


clothes_cnn.load_state_dict(torch.load(os.path.join(pkl_folder, clothes_file),
                                       map_location=dv))
weather_cnn.load_state_dict(torch.load(os.path.join(pkl_folder, weather_file),
                                       map_location=dv))
schedule_cnn.load_state_dict(torch.load(os.path.join(pkl_folder, schedule_file),
                                       map_location=dv))
temperature_max_cnn.load_state_dict(torch.load(os.path.join(pkl_folder, temperature_max_file),
                                       map_location=dv))
temperature_min_cnn.load_state_dict(torch.load(os.path.join(pkl_folder, temperature_min_file),
                                       map_location=dv))


clothes_cnn.eval()
clothes_cnn.to(device)
weather_cnn.eval()
weather_cnn.to(device)
schedule_cnn.eval()
schedule_cnn.to(device)

temperature_max_cnn.eval()
temperature_max_cnn.to(device)
temperature_min_cnn.eval()
temperature_min_cnn.to(device)

def torch_to_list(torch_output):
    num_list = []
    torch_data = torch_output.data[0]
    for i in range(len(torch_data)):
        num_list.append(torch_data[i].item())
    num_list = np.array(num_list)
    return num_list


def exp_list(num_list):
    exp_list = []
    for i in range(len(num_list)):
        exp_list.append(np.exp(num_list[i]))
    return exp_list


def per_list(exp_list):
    per_list = []
    total = 0
    for i in range(len(exp_list)):
        total += round(exp_list[i])
    exp_list /= total
    exp_list *= 100
    for i in range(len(exp_list)):
        per_list.append(round(exp_list[i]))
    return per_list


def make_per_dict(per_list, categories):
    per_dict = OrderedDict()
    for i in range(len(per_list)):
        per_dict[categories[i]] = per_list[i]
    return per_dict

def denormalize(tem):
    return 100 * tem - 50

def bp_analysis(image):
    # Initialize the result
    bp_result = {}

    # output size (batch size, 5)
    clothes_output = clothes_cnn(image)
    weather_output = weather_cnn(image)
    schedule_output = schedule_cnn(image)
    temperature_max_output = temperature_max_cnn(image)
    temperature_min_output = temperature_min_cnn(image)
    
    # CLOTHES
    bp_result['category'] = {}
    _, clothes_predicted = torch.max(clothes_output.data, 1)
    clothes_name = clothes[clothes_predicted.item()]
    clothes_list = torch_to_list(clothes_output)
    clothes_exp = exp_list(clothes_list)
    clothes_per = per_list(clothes_exp)
    clothes_dict = make_per_dict(clothes_per, clothes)
    
    bp_result['category']['predict'] = clothes_name
    bp_result['category']['total'] = clothes_dict
    
    # WEATHER
    bp_result['weather'] = {}
    _, weather_predicted = torch.max(weather_output.data, 1)
    weather_name = weather[weather_predicted.item()]
    weather_list = torch_to_list(weather_output)
    weather_exp = exp_list(weather_list)
    weather_per = per_list(weather_exp)
    weather_dict = make_per_dict(weather_per, weather)
    
    bp_result['weather']['predict'] = weather_name
    bp_result['weather']['total'] = weather_dict
    
    # SCHEDULE
    bp_result['schedule'] = {}
    _, schedule_predicted = torch.max(schedule_output.data, 1)
    schedule_name = schedule[schedule_predicted.item()]
    schedule_list = torch_to_list(schedule_output)
    schedule_exp = exp_list(schedule_list)
    schedule_per = per_list(schedule_exp)
    schedule_dict = make_per_dict(schedule_per, schedule)

    bp_result['schedule']['predict'] = schedule_name
    bp_result['schedule']['total'] = schedule_dict
    
    # TEMPERATURE
    bp_result['temperature'] = {}
    
    ## MAX
    temperature_max = torch_to_list(temperature_max_output)
    temperature_max = round(denormalize(temperature_max[0]))
    bp_result['temperature']['max'] = temperature_max
    
    ## MIN
    temperature_min = torch_to_list(temperature_min_output)
    temperature_min = round(denormalize(temperature_min[0]))
    bp_result['temperature']['min'] = temperature_min
    
    return bp_result

def anaylsis(imName):
    img_files = os.listdir(img_folder)
    print("Using device : ", dv)
    returnString = ""
    data_loader = get_loader(transform=transform,
                         mode='test',
                         batch_size=batch_size,
                         img_folder=img_folder,
                         image_file=img_files)
    
    for batch_i, image in enumerate(data_loader):
        if imName == img_files[batch_i]:
            print("Processing...", imName)
            image = image.to(device)
            json_result = bp_analysis(image)
            returnString = json_result
    return returnString

def anaylsis_with_folder(imName, img_folder):
    img_files = os.listdir(img_folder)
    print("Using device : ", dv)
    returnString = ""
    data_loader = get_loader(transform=transform,
                         mode='test',
                         batch_size=batch_size,
                         img_folder=img_folder,
                         image_file=img_files)
    
    for batch_i, image in enumerate(data_loader):
        if imName == img_files[batch_i]:
            print("Processing...", imName)
            image = image.to(device)
            json_result = bp_analysis(image)
            returnString = json_result
    return returnString
