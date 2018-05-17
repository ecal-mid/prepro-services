Extract model to the model folder:
http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_2018_01_28.tar.gz

Clone and export the object_detection to an object_detection folder:
https://github.com/tensorflow/models/tree/master/research/object_detection

You should then have this project structure
```
.
- model
  - faster_rcnn_resnet101_coco_2018_01_28
- object_detection
  - anchor_generators
  - box_coders
  - ...etc
- protos
```
