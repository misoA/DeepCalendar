# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 15:05:46 2018

@author: hyunb
"""
import os
import json
import math

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms

from data_loader import get_loader
from model import res_fashion_CNN

import configure as cf

# Hyperparameter
'''
batch_size: - duck(It means duck thinks it is useless to explain)
num_epochs: - duck(QUARK!)
save_every: determines how often to save the model weights.
            Recommend that you set save_every=1,
            to save the model weights after each epoch. 
            This way, after the ith epoch, the fashion cnn weights 
            will be saved in the models/ folder as fashion-i.pkl
print_every: determines how often to print the batch loss
log_file: the name of the text file containing - for every step
'''

# Configure file
keyword = cf.keyword
url = cf.url

batch_size = 50
num_epochs = 100
save_every = 5
print_every = 1
log_file = 'training_log.txt'

transform_train = transforms.Compose([ 
    transforms.Resize(256),                          # smaller edge of image resized to 256
    transforms.RandomCrop(224),                      # get 224x224 crop from random location
    transforms.RandomHorizontalFlip(),               # horizontally flip image with probability=0.5
    transforms.ToTensor(),                           # convert the PIL Image to a tensor
    transforms.Normalize((0.485, 0.456, 0.406),      # normalize image for pre-trained model
                         (0.229, 0.224, 0.225))])

# TODO - Change the images file to the folder where the image is
img_folder = url + "/deepc/dataset/preprocess_data/{}".format(keyword)

# TODO - Change the label file where is filled with 
#        [{'image':image_id(str),'label':category index(int)},{},...,{}]
label_file = []
with open(url + "/deepc/{0}_regression/{0}_{1}_train.json".format(keyword, cf.tem), "r") as f:
    label_file = json.load(f)

data_loader = get_loader(transform=transform_train,
                         mode='train',
                         batch_size=batch_size,
                         img_folder=img_folder,
                         label_file=label_file)

fashion_cnn = res_fashion_CNN()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Cuda is available? :", torch.cuda.is_available())
fashion_cnn.to(device)

criterion = nn.MSELoss().cuda() if torch.cuda.is_available() else nn.MSELoss()
params = list(fashion_cnn.linear1.parameters()) + list(fashion_cnn.linear2.parameters()) + \
        list(fashion_cnn.linear3.parameters()) + list(fashion_cnn.linear4.parameters()) + \
        list(fashion_cnn.bn1.parameters()) + list(fashion_cnn.bn2.parameters()) + \
        list(fashion_cnn.bn3.parameters()) + list(fashion_cnn.resnet[-3][-1].parameters()) + \
        list(fashion_cnn.resnet[-2].parameters()) + list(fashion_cnn.resnet[-1].parameters())
        
optimizer = optim.Adam(params, lr=0.001)

# Batch total step
total_step = math.ceil(len(data_loader.dataset) / data_loader.dataset.batch_size)

# Delete annotation if your going to load the pre-trained one
if cf.train_epoch != None:
    load_epoch = cf.train_epoch
    fashion_file = '%s-%d-%s.pkl' % (keyword, load_epoch, cf.tem)
    fashion_cnn.load_state_dict(torch.load(os.path.join('./models', fashion_file)))


# Open the training log file.
f = open(log_file, 'w')

for epoch in range(1, num_epochs+1):
    for i_step in range(1, total_step+1):
        
        # Obtain the batch.
        # images size (batch size, 3, 224, 224)
        # labels size (batch size, 18)
        images, labels = next(iter(data_loader))
        
        images = images.to(device)
        labels = labels.to(device)
        
        fashion_cnn.zero_grad()
        
        # output size (batch size, 18)
        output = fashion_cnn(images)
        
        # Caculate the batch loss
        
#        print(output)
#        print(labels)
        loss = criterion(output, labels)
        
        # Backward pass
        loss.backward()
        
        # Update the parameters in the optimizer
        optimizer.step()
        
        # Training statistics
        stats = 'Epoch [%d/%d], Step [%d/%d], Loss: %.4f' % \
                (epoch, num_epochs, i_step, total_step, loss.item())
                
        # Print training statistics to file.
        f.write(stats + '\n')
        f.flush()
        
        if i_step % print_every == 0:
            print('\r' + stats)
        
        # Save the weights.
        if epoch % save_every == 0:
            torch.save(fashion_cnn.state_dict(), os.path.join('./models', '%s-%d-%s.pkl' % (keyword, epoch, cf.tem)))

f.close()   
