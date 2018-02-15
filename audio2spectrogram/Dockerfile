# Based on https://github.com/abn/scipy-docker-alpine
FROM alpine:latest
MAINTAINER Cyril Diagne <diagne.cyril@gmail.com>

WORKDIR /tmp/audio2spectrogram

# Linking of locale.h as xlocale.h
# This is done to ensure successfull install of python numpy package
# see https://forum.alpinelinux.org/comment/690#comment-690 for more information.

RUN apk --update add --virtual scipy-runtime python py-pip \
    && apk add --virtual scipy-build \
        build-base python-dev openblas-dev freetype-dev pkgconfig gfortran \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pip install --no-cache-dir numpy \
    && pip install --no-cache-dir scipy \
    && apk del scipy-build \
    && apk add --virtual scipy-runtime \
        freetype libgfortran libgcc libpng libstdc++ musl openblas tcl tk \
    && rm -rf /var/cache/apk/*

RUN apk --update add g++ musl-dev libjpeg-turbo-dev python-dev zlib-dev \
    && pip install --no-cache-dir Pillow \
    && rm -rf /var/cache/apk/*

# RUN sudo apt install gcc python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev
RUN pip install --no-cache-dir grpcio

COPY ./ /tmp/audio2spectrogram

ENTRYPOINT ["python", "/tmp/audio2spectrogram/audio2spectrogram.py"]
