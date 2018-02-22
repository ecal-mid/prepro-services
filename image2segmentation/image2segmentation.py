from concurrent import futures

import argparse
import numpy as np
import time
from PIL import Image
from io import BytesIO

import grpc

from protos import bytes2bytes_pb2
from protos import bytes2bytes_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()

import sys
sys.path.insert(0, 'Mask_RCNN')
sys.path.insert(0, 'protos')

from Mask_RCNN import coco
from Mask_RCNN import utils
from Mask_RCNN import model as modellib

model = None


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


class Bytes2Bytes(bytes2bytes_pb2_grpc.Bytes2BytesServicer):

    def Run(self, request, context):
        # Run detection
        buff = BytesIO(request.input)
        img = Image.open(buff)
        results = model.detect([np.asarray(img)], verbose=1)
        r = results[0]
        # rois = r['rois']
        masks = r['masks']
        classes = r['class_ids']
        # scores = r['scores']
        if classes.size == 0:
            # No result found in this frame
            masked_image = np.zeros((img.size[1], img.size[0]))
        else:
            masked_image = np.zeros((masks.shape[0], masks.shape[1]))
            for i in range(classes.size):
                mask = masks[:, :, i]
                masked_image[:, :] = np.where(mask == 1, masks[:, :, i] *
                                              (classes[i] + 127),
                                              masked_image[:, :])

        output = BytesIO()
        img = Image.fromarray(masked_image.astype('uint8'), mode='L')
        img.save(output, format="PNG")
        value = output.getvalue()
        output.close()

        return bytes2bytes_pb2.Bytes2BytesReply(output=value)


def run():

    config = InferenceConfig()
    config.display()
    # Create model object in inference mode.
    print('loading model')
    global model
    model = modellib.MaskRCNN(
        mode="inference", model_dir='/tmp/logs', config=config)
    # Load weights trained on MS-COCO
    print('loading pretrained weights')
    model.load_weights('data/mask_rcnn_coco.h5', by_name=True)
    model.keras_model._make_predict_function()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bytes2bytes_pb2_grpc.add_Bytes2BytesServicer_to_server(
        Bytes2Bytes(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started image2segmentation service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
