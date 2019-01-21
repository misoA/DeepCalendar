# -*- coding: utf-8 -*-

import os
from PIL import Image
import numpy as np
import torch
import torch.utils.data as data

def get_loader(transform,
               mode='train',
               batch_size=1,
               img_folder="/",
               label_file=[],
               num_workers=0):
    """
    Args:
        transform : Image tranform
        mode: One of 'train' or 'test', this arguments are not used at here
        batch_size: Batch Size
        img_folder: the folder path that images are stored
        label_file: The file that stores annotation about the image and label
        num_workers: Number of Subprocesses to use data loading
    
    [Detailed explantion about the label file]
    =========================================================================
    Annotation label_file data structure
    
    list(dict)
    [{'image': image_id(str), 'label', label(int)}]
    
    Ex: [{'image': 'im_1' 'label': 1},
         {'image': 'im_2' 'label': 3},
         {'image': 'im_3' 'label': 7}]
    
    Image id is another expression of image path.
    The loader will load the image by it's path.
    
    label number starts from 0.
    For this label it has 18 different categories.
    So it will start at 0 and end at 17.
    =========================================================================
    
    There is no need to distinguish the train and the test.
    If your going to split to train and test image,
    
    Split the label_file to for example 8:2
    """
    
    assert len(label_file) != 0, "Please fill the label file QUARK!"
      
    dataset = fashion_dataset(transform=transform,
                              mode=mode,
                              batch_size=batch_size,
                              label_file=label_file,
                              img_folder=img_folder)
    
    shuffle = True if mode == 'train' else False

    data_loader = data.DataLoader(dataset=dataset,
                                  batch_size=dataset.batch_size,
                                  shuffle=shuffle,
                                  num_workers=num_workers)

    return data_loader

class fashion_dataset(data.Dataset):
    '''
    Dataset to train the clothes category classification model
    
    The __getitem__ will return 2 variables label and image.

    image = numpy array with size (3, 224, 224)    
    label = Number label file with size (1)  
    '''
    def __init__(self, transform, mode, batch_size, label_file, img_folder):
        self.transform = transform
        self.mode = mode
        self.batch_size = batch_size
        self.label_file = label_file
        self.img_folder = img_folder
    
    def __getitem__(self, index):
        # One hot encoded label
        # [0, 1, 0 ... 0]
        label_num = self.normalize(self.label_file[index]['label'])
        #label = np.zeros(5)
        #label[label_num] = 1
        
        label = torch.tensor(label_num)
        label = torch.unsqueeze(label, dim=0)
        
        #open image
        img_path = os.path.join(self.img_folder,
                                self.label_file[index]['image'])
        PIL_image = Image.open(img_path).convert('RGB')
        orig_image = PIL_image
        image = self.transform(orig_image)
        #print('image size: ', image.size(),
        #      'label size\n: ', label.size())
        
        return image, label
    
    def __len__(self):
        return len(self.label_file)
    
    def normalize(self, tem):
        # min = -50 / max = 50
        tem = float(tem)
        norm = (tem + 50) / 100
        return norm
        
        