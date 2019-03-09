# -*- coding: utf-8 -*-

import os
from PIL import Image
import torch.utils.data as data

def get_loader(transform,
               mode='train',
               batch_size=1,
               img_folder="/",
               image_file=[],
               num_workers=0):
    """
    Args:
        transform : Image tranform
        mode: One of 'train' or 'test', this arguments are not used at here
        batch_size: Batch Size
        img_folder: the folder path that images are stored
        label_file: The file that stores annotation about the image and label
        num_workers: Number of Subprocesses to use data loading
    """
    
    assert len(image_file) != 0, "Please fill the label file QUARK!"
      
    dataset = fashion_dataset(transform=transform,
                              mode=mode,
                              batch_size=batch_size,
                              image_file=image_file,
                              img_folder=img_folder)

    data_loader = data.DataLoader(dataset=dataset,
                                  batch_size=dataset.batch_size,
                                  shuffle=False,
                                  num_workers=num_workers)

    return data_loader

class fashion_dataset(data.Dataset):
    '''
    Dataset to train the clothes category classification model
    
    The __getitem__ will return 2 variables label and image.

    image = numpy array with size (3, 224, 224)    
    '''
    
    def __init__(self, transform, mode, batch_size, image_file, img_folder):
        self.transform = transform
        self.mode = mode
        self.batch_size = batch_size
        self.image_file = image_file
        self.img_folder = img_folder
    
    def __getitem__(self, index):
        
        #open image
        img_path = os.path.join(self.img_folder,
                                self.image_file[index])
        PIL_image = Image.open(img_path).convert('RGB')
        orig_image = PIL_image
        image = self.transform(orig_image)
        #print('image size: ', image.size(),
        #      'label size\n: ', label.size())
        
        return image
    
    def __len__(self):
        return len(self.image_file)

def get_loader_match(transform,
               mode='train',
               batch_size=1,
               img_folder="/",
               image_file=[],
               num_workers=0):

    assert len(image_file) != 0, "Please fill the label file QUARK!"
      
    dataset = fashion_dataset_match(transform=transform,
                              mode=mode,
                              batch_size=batch_size,
                              image_file=image_file,
                              img_folder=img_folder)

    data_loader = data.DataLoader(dataset=dataset,
                                  batch_size=dataset.batch_size,
                                  shuffle=False,
                                  num_workers=num_workers)
    
    return data_loader


class fashion_dataset_match(data.Dataset):
    '''
    Dataset to train the clothes category classification model
    
    The __getitem__ will return 2 variables label and image.

    image = numpy array with size (3, 224, 224)    
    '''
    
    def __init__(self, transform, mode, batch_size, image_file, img_folder):
        self.transform = transform
        self.mode = mode
        self.batch_size = batch_size
        self.image_file = image_file
        self.img_folder = img_folder
    
    def __getitem__(self, index):
        
        #open image
        
        img_path = self.image_file[index]
        img_path_1 = os.path.join(self.img_folder, img_path[0])
        img_path_2 = os.path.join(self.img_folder, img_path[1])
        
        PIL_image_1 = Image.open(img_path_1).convert('RGB')
        orig_image_1 = PIL_image_1
        image_1 = self.transform(orig_image_1)
        
        PIL_image_2 = Image.open(img_path_2).convert('RGB')
        orig_image_2 = PIL_image_2
        image_2 = self.transform(orig_image_2)

        return image_1, image_2
    
    def __len__(self):
        return len(self.image_file)