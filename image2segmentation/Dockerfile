FROM nvidia/cuda:8.0-cudnn6-runtime-ubuntu16.04
MAINTAINER Cyril Diagne <diagne.cyril@gmail.com>

RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    python3.5 python3.5-dev python3-pip python3-tk \
    libjpeg-dev zlib1g-dev \
    build-essential \
    curl \
    libfreetype6-dev \
    libpng12-dev \
    libzmq3-dev \
    pkg-config \
    rsync \
    software-properties-common \
    unzip \
    git \
    && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*


# For convenience, alisas (but don't sym-link) python & pip to python3 & pip3 as recommended in:
# http://askubuntu.com/questions/351318/changing-symlink-python-to-python3-causes-problems
RUN echo "alias python='python3'" >> /root/.bash_aliases
RUN echo "alias pip='pip3'" >> /root/.bash_aliases

RUN pip3 install --no-cache-dir --upgrade \
    pip \
    setuptools

RUN pip3 install --no-cache-dir --upgrade \
    Pillow \
    numpy \
    requests \
    Cython \
    h5py \
    pandas \
    scipy \
    sklearn \
    scikit-image \
    matplotlib

RUN pip3 install --no-cache-dir --upgrade \
    tensorflow-gpu==1.4 \
    pydot_ng \
    keras

RUN pip3 install --no-cache-dir --upgrade \
    grpcio

#
# PyCocoTools
#
# Using a fork of the original that has a fix for Python 3.
# I submitted a PR to the original repo (https://github.com/cocodataset/cocoapi/pull/50)
# but it doesn't seem to be active anymore.
RUN pip3 install --no-cache-dir git+https://github.com/waleedka/coco.git#subdirectory=PythonAPI


COPY Mask_RCNN /image2segmentation/Mask_RCNN
COPY data /image2segmentation/data
COPY protos /image2segmentation/protos
COPY image2segmentation.py /image2segmentation/

RUN touch /image2segmentation/Mask_RCNN/__init__.py

WORKDIR /image2segmentation

ENTRYPOINT ["python3", "image2segmentation.py"]
