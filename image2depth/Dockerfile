FROM tensorflow/tensorflow:1.8.0-gpu
MAINTAINER Cyril Diagne <diagne.cyril@gmail.com>

RUN apt-get update

RUN pip install --no-cache-dir --upgrade \
    grpcio

RUN pip install --no-cache-dir --upgrade \
    numpy

WORKDIR /image2depth

COPY FCRN_DepthPrediction FCRN_DepthPrediction
COPY protos protos
COPY image2depth.py .

ENTRYPOINT ["python", "image2depth.py"]
