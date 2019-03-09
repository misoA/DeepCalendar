# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request
from resources.S3Image import put_image_to_s3, get_image_from_s3

class DetectImage(Resource):
    def get(self):
        detectImName = request.args.get('detectImName')
        detectImList = detected_img_crop(detectImName)
        return {"list": detectImList}
    
    def post(self):
        detectImName = request.args.get('detectImName')
        detectImList = detected_img_crop(detectImName)
        return {"list": detectImList}
    

# Import packages
import cv2
import numpy as np
import os
import sys
import tensorflow as tf


import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
from matplotlib import pyplot as plt

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
sys.path.insert(0, 'PUT_YOUR_PATH')

# Import utilites
from utils import label_map_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'
imsave_path = 'PUT_YOUR_PATH'
im_link_url = 'PUT_YOUR_PATH'

def detected_img_crop(detectImName):
    
    get_image_from_s3(detectImName, os.path.join(imsave_path, detectImName))

    # Grab path to current working directory
    CWD_PATH = os.getcwd()
    
    # Path to frozen detection graph .pb file, which contains the model that is used
    # for object detection.
    PATH_TO_CKPT = os.path.join(CWD_PATH,'tensorflow',MODEL_NAME,'frozen_inference_graph.pb')
    
    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,'tensorflow','training','labelmap.pbtxt')
    
    # Path to image
    PATH_TO_IMAGE = os.path.join(imsave_path, detectImName)
    print('start image : ' + detectImName)
    
    # Number of classes the object detector can identify
    NUM_CLASSES = 5
    
    # Load the label map.
    # Label maps map indices to category names, so that when our convolution
    # network predicts `5`, we know that this corresponds to `king`.
    # Here we use internal utility functions, but anything that returns a
    # dictionary mapping integers to appropriate string labels would be fine
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    
    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    
        sess = tf.Session(graph=detection_graph)
    
    # Define input and output tensors (i.e. data) for the object detection classifier
    
    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    
    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    
    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    
    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    
    # Load image using OpenCV and
    # expand image dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    image = cv2.imread(PATH_TO_IMAGE)
    image_expanded = np.expand_dims(image, axis=0)
    
    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(   
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})
    
    fig = plt.figure()
    
    max_boxes_to_draw = 5
    min_score_thresh=.8
    sq_boxes = np.squeeze(boxes)
    
    saveImList = list()
    for i in range(min(max_boxes_to_draw, sq_boxes.shape[0])):
        if scores is None or np.squeeze(scores)[i] > min_score_thresh:
            (ymin, xmin, ymax, xmax) = tuple(sq_boxes[i].tolist())
            (im_height, im_width) = image.shape[:2]
            (xminn, xmaxx, yminn, ymaxx) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
            
            crop_image = tf.image.crop_to_bounding_box(
                    image
                    , np.int32(yminn)
                    , np.int32(xminn)
                    , np.int32(ymaxx-yminn)
                    , np.int32(xmaxx-xminn))
            sess = tf.Session()
            img_data = sess.run(crop_image)
            sess.close()
            
            fig.add_subplot()
            class_name = category_index[np.squeeze(classes).astype(np.int32)[i]]['name']
            print(class_name, str(int(100*np.squeeze(scores)[i])) + '%')
            #plt.imshow(cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB))
            #plt.show()
            
            img_name = detectImName[:-4] + '_' + (class_name[:-1] if class_name.endswith('_') else class_name) + '_' + str(i) + detectImName[-4:]
            saveImList.append(img_name)
            plt.imsave(
                    os.path.join(imsave_path, img_name)
                    , cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB))
    
    returnImList = list()
    for img in saveImList:
        put_image_to_s3(os.path.join(imsave_path, img), img)
        returnImList.append(im_link_url + img)
        
    return returnImList

