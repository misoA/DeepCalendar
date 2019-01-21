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

batch_size = 50

# TODO - Change the images file to the folder where the image is
img_folder = url + "/deepc/dataset/preprocess_data/{}".format(keyword)


# TODO - Change the label file where is filled with 
#        [{'image':image_id(str),'label':category index(int)},{},...,{}]

label_file = []
                     
with open(url + "/deepc/{0}/{0}_test.json".format(keyword), "r") as f:
    label_file = json.load(f)

data_loader = get_loader(transform=transform_test,
                         mode='test',
                         batch_size=batch_size,
                         img_folder=img_folder,
                         label_file=label_file)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the pre-trained one
dv = "cuda" if torch.cuda.is_available() else 'cpu'

fashion_cnn = res_fashion_CNN()
criterion = nn.MSELoss().cuda() if torch.cuda.is_available() else nn.MSELoss()

# Load the pre-trained one
load_epoch = cf.inference_epoch
fashion_file = '%s-%d.pkl' % (keyword, load_epoch)
fashion_cnn.load_state_dict(torch.load(os.path.join('./models', fashion_file),
                                       map_location=dv))

fashion_cnn.eval()
fashion_cnn.to(device)

#dtype = torch.cuda.FloatTensor if torch.cuda.is_available else torch.FloatTensor
test_loss = torch.zeros(1)
reg_correct = 0
reg_total = 0

f = open('{}_test_result.json'.format(keyword), 'w')
result_list = []
index = 0

def torch_to_list(t_list):
    m_list = []
    for i in range(len(t_list)):
        match_rate = t_list[i].item()
        match_rate = round(match_rate, 2)
        m_list.append(match_rate)
    return m_list
    

for batch_i, data in enumerate(data_loader):
    # Obtain the batch.
    # images size (batch size, 3, 224, 224)
    # labels size (batch size, 5)
    images_1, images_2, labels = data
    
    images_1 = images_1.to(device)
    images_2 = images_2.to(device)
    labels = labels.to(device)
        
    # output size (batch size, 5)
    output = fashion_cnn((images_1, images_2))
    
    # Calculate the batch loss
    loss = criterion(output, labels)
    
    # Update average test loss
    test_loss = test_loss + ((torch.ones(1) / (batch_i + 1)) * (loss.item() - test_loss))
    
    # get the predicted temperature from the maximum value in the output_list of class scores
    # (batch size, 1)
    output_list = list(output.data)
    label_list = list(labels.data)
    
    # Transform torch list to list and denomrmalize and round.
    output_list = torch_to_list(output_list)
    label_list = torch_to_list(label_list)
    for i in range(len(output_list)):
        pre_dict = {}
        pre_dict['index'] = index
        pre_dict['predict'] = output_list[i]
        pre_dict['label'] = label_list[i]
        index += 1
        result_list.append(pre_dict)
    
    # compare predictions to true label
    # correct = [0,1,1,...,1,0,1]
    correct = []
    output_list = np.array(output_list)
    label_list = np.array(label_list)
    match = output_list == label_list
    correct = list(match)
    #if batch_i % 100 == 0:
    print('\nbatch step: ', batch_i+1)
    print('test_loss: ', test_loss)
    print('label :', label_list)
    print('The index where matched :', list(np.where(match)))
    
    # calculate test accuracy for each object class
    for i in range(len(correct)):
        reg_correct += correct[i]
        reg_total += 1
    print('correct :', reg_correct)
    print('total :', reg_total)

print('Test Loss: {:.6f}\n'.format(test_loss.numpy()[0]))

if reg_total > 0:
    print('Test Accuracy of match (Overall): %2d%%' % (100 * reg_correct / reg_total))
else:
    print('Test Accuracy of match: N/A (no training examples)')

f.write(json.dumps(result_list))
print("Result written in result file")