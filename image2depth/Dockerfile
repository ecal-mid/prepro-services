FROM tensorflow/tensorflow:1.8.0-gpu
MAINTAINER Cyril Diagne <diagne.cyril@gmail.com>

RUN apt-get update

RUN pip3 install --no-cache-dir --upgrade \
    grpcio

WORKDIR /image2depth

COPY FCRN-DepthPrediction .
COPY protos protos
COPY image2segmentation.py /image2segmentation/

RUN touch /image2segmentation/Mask_RCNN/__init__.py

WORKDIR /image2segmentation

ENTRYPOINT ["python3", "image2segmentation.py"]
