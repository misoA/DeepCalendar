# Deep Calendar Detection

##### 이미지에서 상의(top)/하의(bottom)를 Object Detection(tensorflow-Faster RCNN), 잘라낸 이미지를 저장하여 이후 학습에 사용함.


## Detection 사용 기술
TensorFlow의 ObjectDetection API를 사용하여 이미지에서 의상의 상의와 하의를 Detection 하는 방법입니다.(Windows/Linux OS)
TensorFlow `Mode Zoo`에서 `Faster-RCNN-Inception-V2-COCO` 모델을 다운로드하여 사용하였으며, `SSD-MobileNet` 등 다른 모델을 사용할 수 있습니다.
(_[TensorFlow Faster-RCNN-Inception-V2-COCO Model 다운로드](http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz)_)
1. 이미지의 모든 개체(상/하의) detecting/boxing/image_cropping/image_server_uploading
2. 이미지의 개체(상/하의) 중 가장 정확도가 높은 것을 detecting/boxing/image_cropping/image_server_uploading

## Tutorial
아래의 github을 참조하여 Custom Object Detection 모델을 학습함  
(ref : https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)  
학습 소스코드는 위의 링크를 참조  
학습된 `frozen_inference_graph`와 `labelmap`을 이용하여 신규 이미지에 대해 Detection 실시  
```
python OBJECT_DETECTION_FOLDER_PWD/Object_detection_image.py
```
_이 때 IMAGE_NAME 변수와 신규 이미지 파일 이름을 일치하도록 해야함_



## License
![main page](../bplogo.jpg)

