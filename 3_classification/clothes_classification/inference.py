# -*- coding: utf-8 -*-

import os
import json
import numpy as np
from data_loader import get_loader
from model import res_fashion_CNN

import torch
import torch.nn as nn
from torchvision import transforms

import configure as cf

transform_test = transforms.Compose([ 
    transforms.Resize(256),                          # smaller edge of image resized to 256
    transforms.RandomCrop(224),                      # get 224x224 crop from random location
    transforms.RandomHorizontalFlip(),               # horizontally flip image with probability=0.5
    transforms.ToTensor(),                           # convert the PIL Image to a tensor
    transforms.Normalize((0.485, 0.456, 0.406),      # normalize image for pre-trained model
                         (0.229, 0.224, 0.225))])
# Configure file
keyword = cf.keyword
url = cf.url
categories = cf.categories

batch_size = 50

# TODO - Change the images file to the folder where the image is
img_folder = url + "/deepc/dataset/preprocess_data/{}".format(keyword)


# TODO - Change the label file where is filled with 
#        [{'image':image_id(str),'label':category index(int)},{},...,{}]

label_file = []
                     
with open(url + "/deepc/{0}_classification/{0}_test.json".format(keyword), "r") as f:
    label_file = json.load(f)

category_len = len(categories)

data_loader = get_loader(transform=transform_test,
                         mode='test',
                         batch_size=batch_size,
                         img_folder=img_folder,
                         label_file=label_file)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

fashion_cnn = res_fashion_CNN()
criterion = nn.CrossEntropyLoss().cuda() if torch.cuda.is_available() else nn.CrossEntropyLoss()


# Load the pre-trained one
dv = "cuda" if torch.cuda.is_available() else 'cpu'

load_epoch = cf.inference_epoch
fashion_file = '%s-%d.pkl' % (keyword, load_epoch)
fashion_cnn.load_state_dict(torch.load(os.path.join('./models', fashion_file),
                                       map_location=dv))

fashion_cnn.eval()
fashion_cnn.to(device)

#dtype = torch.cuda.FloatTensor if torch.cuda.is_available else torch.FloatTensor
test_loss = torch.zeros(1)
class_correct = list(0. for i in range(category_len))
class_total = list(0. for i in range(category_len))

f = open('{}_test_result.json'.format(keyword), 'w')
result_list = []
index = 0

for batch_i, data in enumerate(data_loader):
    # Obtain the batch.
    # images size (batch size, 3, 224, 224)
    # labels size (batch size, 5)
    images, labels = data
    
    images = images.to(device)
    labels = labels.to(device)
        
    # output size (batch size, 5)
    output = fashion_cnn(images)
    
    # Calculate the batch loss
    loss = criterion(output, labels)
    
    # Update average test loss
    test_loss = test_loss + ((torch.ones(1) / (batch_i + 1)) * (loss.item() - test_loss))
    
    # get the predicted class from the maximum value in the output_list of class scores
    # (batch size, 1)
    _, predicted = torch.max(output.data, 1)
    pre_list = list(predicted.cpu().numpy())
    lab_list = list(labels.cpu().numpy())
    for i in range(len(pre_list)):
        pre_dict = {}
        pre_dict['index'] = index
        pre_dict['label'] = categories[lab_list[i]]
        pre_dict['predict'] = categories[pre_list[i]]
        index += 1
        result_list.append(pre_dict)
    
    # compare predictions to true label
    # correct = [0,1,1,...,1,0,1]
    correct = 0
    correct += (predicted == labels)
    #if batch_i % 100 == 0:
    print('\nbatch step: ', batch_i+1)
    #print('loss: ', loss)
    print('test_loss: ', test_loss)
    print('label :', labels)
    
    # calculate test accuracy for each object class
    for i in range(len(labels)):
        label = labels.data[i].item()
        class_correct[label] += correct[i].item()
        class_total[label] += 1
    print('class correct :', class_correct)
    print('class total :', class_total)

print('Test Loss: {:.6f}\n'.format(test_loss.numpy()[0]))

for i in range(category_len):
    if class_total[i] > 0:
        print('Test Accuracy of %5s: %2d%% (%2d/%2d)' % (
                categories[i], 100 * class_correct[i] / class_total[i],
                np.sum(class_correct[i]), np.sum(class_total[i])))
    else:
        print('Test Accuracy  of %5s: N/A (no training examples)' % (categories[i]))

print('\nTest Accuracy (Overall): %2d%% (%2d/%2d)' % (
        100. * np.sum(class_correct) / np.sum(class_total),
        np.sum(class_correct), np.sum(class_total)))

f.write(json.dumps(result_list))
print("Result written in result file")