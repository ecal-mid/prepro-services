FROM nvidia/cuda:8.0-cudnn6-devel-ubuntu16.04

RUN apt-get update && apt-get install -y \
  rsync \
  htop \
  git \
  openssh-server \
  python-pip \
  ffmpeg

RUN pip install --upgrade pip

RUN pip install http://download.pytorch.org/whl/cu80/torch-0.2.0.post3-cp27-cp27mu-manylinux1_x86_64.whl
RUN pip install \
  torchvision \
  cffi \
  tensorboardX \
  tqdm \
  scipy \
  scikit-image \
  colorama==0.3.7 \
  setproctitle \
  pytz \
  ipython
RUN pip install grpcio

COPY flownet2-pytorch video2flow/flownet2-pytorch
COPY FlowNet2_checkpoint.pth.tar /video2flow/flownet2-pytorch/

WORKDIR /video2flow

RUN cd flownet2-pytorch && bash install.sh && cd ..

RUN apt-get -y install zip python-tk
RUN pip install pypng
COPY src/ /video2flow/

ENTRYPOINT ["python", "video2flow.py"]
