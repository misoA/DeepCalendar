# -*- coding: utf-8 -*-

import json

import configure as cf

# Configure file
keyword = cf.keyword
url = cf.url
categories = cf.categories

dirpath = url + '/deepc/{0}_classification/{0}_test_result.json'.format(keyword)

label_file = []

with open(dirpath, "r") as f:
    label_file = json.load(f)

label_file.sort(key=lambda x: x['label'])

f = open("analysis.txt", "w")

for i in range(len(label_file)):
    result = "Index is {} and it's {} and the predicted is {}\n".format(label_file[i]['index'], label_file[i]['label'], label_file[i]['predict'])
    f.write(result)
    f.flush

'''
analysis_file = []

with open(url + "/deepc/catergory_classification/{}_test.json".format(keyword), "r") as f:
    analysis_file = json.load(f)

investigate = [180]
for i in investigate:
    print(analysis_file[i]['image'])
'''

