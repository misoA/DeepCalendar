# -*- coding: utf-8 -*-

# [{'image_1': 'M_25025_25025_3_500.jpg',
#   'image_2': 'M_21225_25025_3_500.jpg',
#   'label': 1}]

import os
import math
import json
import shutil

import configure as cf

# Configure file
keyword = cf.keyword
url = cf.url


dirpath = url + "/deepc/dataset/raw_data/{}".format(keyword)
category_list = os.listdir(dirpath)

for category in category_list:
    category_path = os.path.join(dirpath, category)
    img_list = os.listdir(category_path)
    img_len = len(img_list)
    
    match_list = []

    for i in range(int(img_len / 2)):
        img_1_id = i * 2
        img_2_id = img_1_id + 1
    
        match_list.append({'image_1': img_list[img_1_id],
                           'image_2': img_list[img_2_id],
                           'label': category})
    
    print(match_list[:10])
    with open(url + "/deepc/{0}/dataset/{0}_{1}.json".format(keyword, category), 'w') as f:
        f.write(json.dumps(match_list))


# Choose the ratio between train and test
train_test_ratio = 0.8

label_train = []
label_test = []


# Make the train and test json file from each category json file

for category in category_list:
    with open(url + "/deepc/{0}/dataset/{0}_{1}.json".format(keyword, category), 'r') as f:
        match_list = json.load(f)
        match_len = len(match_list)
        print("Match list rate is {} length is :".format(category), match_len)
        bound_num = math.ceil(match_len * train_test_ratio)
        
        print('Label train length will be :', bound_num)
        print('Label test length will be :', match_len - bound_num)
        print('\n')
        
        label_train.extend(match_list[:bound_num])
        label_test.extend(match_list[bound_num:])


print("Length of train file is :", len(label_train))
print("Length of test file is :", len(label_test))
print("Spliting Done!")
    
with open(url + "/deepc/{0}/{0}_train.json".format(keyword), "w") as f:
    f.write(json.dumps(label_train))
    
with open(url + "/deepc/{0}/{0}_test.json".format(keyword), "w") as f:
    f.write(json.dumps(label_test))
    

# Move the files in raw_data folder to pre_process folder
print("\nCoping the raw_data to preprocess data\n\n")
prepath = url + '/deepc/dataset/preprocess_data/{}'.format(keyword)
if not os.path.isdir(prepath):
    os.makedirs(prepath)

for category in category_list:
    before_copy = len(os.listdir(prepath))
    category_path = os.path.join(dirpath, category)
    img_list = os.listdir(category_path)
    print("Image length of {0} is {1}".format(category, len(img_list)))
    for img in img_list:
        src = os.path.join(category_path, img)
        dst = prepath
        shutil.copy2(src, dst)
    after_copy = len(os.listdir(prepath))
    print("Image copied total number is : {}\n\n".format(after_copy - before_copy))
