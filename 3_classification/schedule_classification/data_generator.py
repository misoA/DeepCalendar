# -*- coding: utf-8 -*-

# [{'image': 'M_25025_25025_3_500.jpg', 'label': 0}]
# {0: 'cloudy', 1: 'rain', 2: 'snow', 3: 'sunny'}

import os
import math
import json
import shutil

import configure as cf

# Configure file
keyword = cf.keyword
url = cf.url
categories = cf.categories

dirpath = url + "/deepc/dataset/raw_data/{}".format(keyword)

categoryList = os.listdir(dirpath)
categoryDict = dict()

# Choose the ratio between train and test
train_test_ratio = 0.8

label_train = []
label_test = []

# Make the json file for each category
for index, category in enumerate(categoryList):
    categoryDict[index] = category

for key in categoryDict.keys():
    category_list = []
    label_path = os.path.join(dirpath, categoryDict[key])
    label_list = os.listdir(label_path)
    for img_name in label_list:
        category_list.append({'image':img_name, 'label':key})
    with open(url + "/deepc/{0}_classification/dataset/{0}_{1}.json".format(keyword, categoryDict[key]), "w") as f:
        f.write(json.dumps(category_list))
    print(category_list[:10])
    print("Saved {}_{}.json file\n".format(keyword, categoryDict[key]))


# Make the train and test json file from each category json file
for category in categories:
    with open(url + "/deepc/{0}_classification/dataset/{0}_{1}.json".format(keyword, category), "r") as f:
        label_file = json.load(f)
        label_len =  len(label_file)
        print('CATEGORY - {}'.format(category))
        print('Label file total length is :', label_len)
        bound_num = math.ceil(label_len * train_test_ratio)
        print('Label train length will be :', bound_num)
        print('Label test length will be :', label_len - bound_num)
        print('\n')
        
        label_train.extend(label_file[:bound_num])
        label_test.extend(label_file[bound_num:])


print("Length of train file is :", len(label_train))
print("Length of test file is :", len(label_test))
print("Spliting Done!")
    
with open(url + "/deepc/{0}_classification/{0}_train.json".format(keyword), "w") as f:
    f.write(json.dumps(label_train))
    
with open(url + "/deepc/{0}_classification/{0}_test.json".format(keyword), "w") as f:
    f.write(json.dumps(label_test))
    

# Move the files in raw_data folder to pre_process folder
print("\nCoping the raw_data to preprocess data\n\n")
prepath = url + '/deepc/dataset/preprocess_data/{}'.format(keyword)
if not os.path.isdir(prepath):
    os.makedirs(prepath)

for category in categories:
    category_path = os.path.join(dirpath, category)
    image_list = os.listdir(category_path)
    print("Image length is {} at {}".format(len(image_list), category))
    before_copy = len(os.listdir(prepath))
    for image in image_list:
        src = os.path.join(category_path, image)
        dst = prepath
        shutil.copy2(src, dst)
    after_copy = len(os.listdir(prepath))
    print("Image copied total number is : {}\n\n".format(after_copy - before_copy))
