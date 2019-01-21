#-*- coding: utf-8 -*-

# This file is made to configure every file number at one place

# [1] choose the keyword
# [2] make the dataset file and category folder to keyword / keyword_classifcation
# [3] Choose the PC number
# [4] Choose the train load_epoch [option]
# [5] choose the inference load_epoch

import os

keyword = 'temperature'

# Choose the place you are training at
# AWS : 0, Own PC : 1
PC = 0

# MAX : 0, MIN : 1
TEM = 1

train_epoch = None
inference_epoch = 30

path_list = ["/jet/prs/workspace/fashion-cnn", "C:"]
tem_list = ['max', 'min']

url = path_list[PC]
tem = tem_list[TEM]

dirpath = url + "/deepc/dataset/raw_data/{}".format(keyword)

categories = os.listdir(dirpath)

