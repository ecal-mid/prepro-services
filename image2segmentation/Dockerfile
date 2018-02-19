FROM waleedka/modern-deep-learning

RUN pip3 install --no-cache grpcio

COPY Mask_RCNN /image2segmentation/Mask_RCNN
COPY data /image2segmentation/data
COPY protos /image2segmentation/protos
COPY image2segmentation.py /image2segmentation/

RUN touch /image2segmentation/Mask_RCNN/__init__.py

WORKDIR /image2segmentation

ENTRYPOINT ["python3", "image2segmentation.py"]
