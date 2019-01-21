# -*- coding: utf-8 -*-

# [{'image': 'M_25025_25025_3_500.jpg', 'label': temperature}]

import os
import math
import json
import shutil
import urllib
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

#sys.path.append("C:\deepc\temperature_regression")

import configure as cf
#import datetime


# Configure file
keyword = cf.keyword
url = cf.url
dateList = cf.categories

dirpath = url + "/deepc/dataset/raw_data/{}".format(keyword)

#dateList = os.listdir(dirpath)

# {'2018-03-22': 12, '2018-03-23': 15, ... , '2018-08-22': 37}
date_tem_max_Dict = dict()
date_tem_min_Dict = dict()

# Choose the ratio between train and test
train_test_ratio = 0.8

label_train_max = []
label_test_max = []

label_train_min = []
label_test_min = []

# TODO : Make a function that get inputs a date and return the temperature
def get_tem(date):
    url = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?'+ 'key=aac4958d55af4ad1a3162729180309&q=Seoul&date=' + date
    
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'lxml-xml')
        maxC = soup.find('maxtempC').text
        minC = soup.find('mintempC').text
    return maxC, minC

# Make the json file for each category
for date in dateList:
    tem = get_tem(date)
    date_tem_max_Dict[date] = tem[0] # max
    date_tem_min_Dict[date] = tem[1] # min

for date in date_tem_max_Dict.keys():
    date_list_max = []
    date_list_min = []
    date_path = os.path.join(dirpath, date)
    img_list = os.listdir(date_path)
    for img in img_list:
        date_list_max.append({'image': img, 'label': date_tem_max_Dict[date]})
        date_list_min.append({'image': img, 'label': date_tem_min_Dict[date]})

    with open(url + "/deepc/{0}_regression/dataset/{0}_{1}_max.json".format(keyword, date), 'w') as f:
        f.write(json.dumps(date_list_max))
    print("Saved {}_{}_max.json file\n".format(keyword, date))

    with open(url + "/deepc/{0}_regression/dataset/{0}_{1}_min.json".format(keyword, date), 'w') as f:
        f.write(json.dumps(date_list_min))
    print("Saved {}_{}_min.json file\n".format(keyword, date))
    
    print("Date list max \n\n", date_list_max[:10])
    print("Date list min \n\n", date_list_min[:10])


# Make the train and test json file from each category json file
for date in date_tem_max_Dict.keys():
    with open(url + "/deepc/{0}_regression/dataset/{0}_{1}_max.json".format(keyword, date), "r") as f:
        label_file = json.load(f)
        label_len =  len(label_file)
        print('DATE - {}'.format(date))
        print('Label file total length is :', label_len)
        bound_num = math.ceil(label_len * train_test_ratio)
        print('Label train length will be :', bound_num)
        print('Label test length will be :', label_len - bound_num)
        print('\n')
        
        label_train_max.extend(label_file[:bound_num])
        label_test_max.extend(label_file[bound_num:])
        
print("Length of train max file is :", len(label_train_max))
print("Length of test max file is :", len(label_test_max))
print("Spliting Done!")

for date in date_tem_min_Dict.keys():
    with open(url + "/deepc/{0}_regression/dataset/{0}_{1}_min.json".format(keyword, date), "r") as f:
        label_file = json.load(f)
        label_len =  len(label_file)
        print('DATE - {}'.format(date))
        print('Label file total length is :', label_len)
        bound_num = math.ceil(label_len * train_test_ratio)
        print('Label train length will be :', bound_num)
        print('Label test length will be :', label_len - bound_num)
        print('\n')
        
        label_train_min.extend(label_file[:bound_num])
        label_test_min.extend(label_file[bound_num:])

print("Length of train min file is :", len(label_train_min))
print("Length of test min file is :", len(label_test_min))
print("Spliting Done!")

    
with open(url + "/deepc/{0}_regression/{0}_max_train.json".format(keyword), "w") as f:
    f.write(json.dumps(label_train_max))
with open(url + "/deepc/{0}_regression/{0}_max_test.json".format(keyword), "w") as f:
    f.write(json.dumps(label_test_max))
    
with open(url + "/deepc/{0}_regression/{0}_min_train.json".format(keyword), "w") as f:
    f.write(json.dumps(label_train_min))
with open(url + "/deepc/{0}_regression/{0}_min_test.json".format(keyword), "w") as f:
    f.write(json.dumps(label_test_min))

# Move the files in raw_data folder to pre_process folder
print("\nCoping the raw_data to preprocess data\n\n")
prepath = url + '/deepc/dataset/preprocess_data/{}'.format(keyword)
if not os.path.isdir(prepath):
    os.makedirs(prepath)

for date in date_tem_max_Dict.keys():
    date_path = os.path.join(dirpath, date)
    image_list = os.listdir(date_path)
    print("Image length is {} at {}".format(len(image_list), date))
    before_copy = len(os.listdir(prepath))
    for image in image_list:
        src = os.path.join(date_path, image)
        dst = prepath
        shutil.copy2(src, dst)
    after_copy = len(os.listdir(prepath))
    print("Image copied total number is : {}\n\n".format(after_copy - before_copy))
