# FROM idock.daumkakao.io/kakaobrain/deepcloud-sshd:openpose-preprocess
# FROM tensorflow/tensorflow:1.8.0-gpu
FROM tensorflow/tensorflow:1.8.0

RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    git \
		libopencv-dev python-opencv python-tk \
		swig \
		&& \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

COPY tf-pose-estimation /root/tf-pose-estimation
WORKDIR /root/tf-pose-estimation/

RUN cd /root/tf-pose-estimation/ && pip install -r requirements.txt

WORKDIR /root/tf-pose-estimation/src/pafprocess
RUN swig -python -c++ pafprocess.i && python setup.py build_ext --inplace

RUN pip install --no-cache-dir --upgrade \
    grpcio

WORKDIR /root
COPY model.py model.py
COPY image2pose.py image2pose.py

ENTRYPOINT ["python", "image2pose.py"]
