FROM tensorflow/tensorflow:1.11.0-gpu

RUN apt-get update
RUN apt-get --yes install python-opencv

RUN pip install --no-cache-dir --upgrade \
    grpcio \
    numpy \
    scipy

WORKDIR /image2faces

COPY facenet-master facenet-master
COPY model model
COPY protos protos
COPY model.py .
COPY image2faces_grpc.py .

ENTRYPOINT ["python", "image2faces_grpc.py"]
