# From chriamue/openpose
FROM nvidia/cuda:8.0-cudnn6-devel-ubuntu16.04

RUN apt-get update && apt-get install -y \
      build-essential \
      cmake \
      git \
      libatlas-base-dev \
      libatlas-dev \
      libboost-all-dev \
      libgflags-dev \
      libgoogle-glog-dev \
      libhdf5-dev \
      libleveldb-dev \
      liblmdb-dev \
      libopencv-dev \
      libprotobuf-dev \
      libsnappy-dev \
      lsb-release \
      protobuf-compiler \
      python-dev \
      python-numpy \
      python-pip \
      python-setuptools \
      python-scipy \
      sudo \
      wget \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

#RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git
#RUN cd openpose && git checkout cmake && git pull origin cmake && mkdir -p build && cd build \
#    && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j"$(nproc)"

COPY openpose openpose

RUN cd openpose && mkdir -p build && cd build \
    && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j"$(nproc)"

RUN cd openpose/models && ./getModels.sh

WORKDIR /openpose

RUN pip install grpcio

COPY ./protos ./protos
COPY ./video2openpose.py ./video2openpose.py

ENTRYPOINT ["python", "video2openpose.py"]
