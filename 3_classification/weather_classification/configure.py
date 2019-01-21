# -*- coding: utf-8 -*-

# This file is made to configure every file number at one place

# [1] choose the keyword
# [2] make the dataset file and category folder to keyword / keyword_classifcation
# [3] Choose the PC number
# [4] Choose the train load_epoch [option]
# [5] choose the inference load_epoch

import os

keyword = 'weather'

# Choose the place you are training at
# AWS : 0, Own PC : 1

PC = 1
train_epoch = None
inference_epoch = 3

path_list = ["/jet/prs/workspace/fashion-cnn", "C:"]
url = path_list[PC]
dirpath = url + "/deepc/dataset/raw_data/{}".format(keyword)

# If you have only model and no dataset then you should enter manually
#categories = ['cloudy',
#              'rain',
#              'snow',
#              'sunny']

categories = os.listdir(dirpath)
#categories_len = len(categories)

