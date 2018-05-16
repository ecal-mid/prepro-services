FROM tensorflow/tensorflow:1.8.0-gpu

RUN apt-get update

RUN pip install --no-cache-dir --upgrade \
    grpcio \
    numpy

WORKDIR /image2features

COPY model model
COPY protos protos
COPY image2features.py .

ENTRYPOINT ["python", "image2features.py"]
