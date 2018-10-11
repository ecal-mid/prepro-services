from concurrent import futures

import argparse
import base64
import numpy as np
import time
from PIL import Image
from io import BytesIO

import grpc

from protos import image2faces_pb2
from protos import image2faces_pb2_grpc

import model

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
parser.add_argument(
    '-m',
    '--pretrained_model_path',
    default='model/20180402-114759',
    help='Pretrained Facenet model Path')
args = parser.parse_args()

import sys
sys.path.insert(0, 'protos')


class Image2Faces(image2faces_pb2_grpc.Image2FacesServicer):
    def Run(self, request, context):
        """Runs the detection and returns a Image2FacesReply."""
        # Run detection.
        buff = BytesIO(request.input)
        img = Image.open(buff)
        img_array = np.array(img, np.uint8)
        result = model.run(img_array)
        print('found %s faces' % len(result))
        # Build Response proto.
        resp = image2faces_pb2.Image2FacesReply()
        for f in result:
            x1, y1, x2, y2, features = f
            face = resp.faces.add()
            face.x1 = x1
            face.y1 = y1
            face.x2 = x2
            face.y2 = y2
            face.facenet = base64.b64encode(features).decode('utf-8')
            # face.facenet.extend(facenet)
        # Send Response.
        return resp


def run():
    # Load the model.
    model.load(args.pretrained_model_path)
    # Initialize the server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image2faces_pb2_grpc.add_Image2FacesServicer_to_server(
        Image2Faces(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started image2faces service on port %i' % args.port)
    # Start infinite loop.
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
