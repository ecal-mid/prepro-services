# FROM tensorflow/tensorflow:1.8.0-gpu
FROM tensorflow/tensorflow:1.8.0

RUN apt-get update

RUN apt-get install -y \
    protobuf-compiler \
    python-pil \
    python-lxml \
    python-tk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade \
    grpcio \
    numpy

WORKDIR /image2detection

COPY object_detection object_detection
COPY model model
COPY protos protos
COPY model.py .
COPY image2detection.py .

ENTRYPOINT ["python", "image2detection.py"]
