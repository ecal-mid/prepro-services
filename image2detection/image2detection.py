from concurrent import futures

import argparse
import numpy as np
import time
from PIL import Image
from io import BytesIO

import grpc

from protos import bytes2boxes_pb2
from protos import bytes2boxes_pb2_grpc

import model

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()

import sys
sys.path.insert(0, 'protos')


class Bytes2Boxes(bytes2boxes_pb2_grpc.Bytes2BoxesServicer):

    def Run(self, request, context):
        # Run detection
        buff = BytesIO(request.input)
        img = Image.open(buff)
        result = model.run(img)

        # Send response
        num_detections = result['num_detections']
        resp = bytes2boxes_pb2.Bytes2BoxesReply()
        for i in range(num_detections):
            detect = resp.detections.add()
            detected_class = result['detection_classes'][i]
            detect.category = model.category_index[detected_class]['name']
            detect.score = result['detection_scores'][i]
            detected_box = result['detection_boxes'][i]
            detect.x = detected_box[0]
            detect.y = detected_box[1]
            detect.width = detected_box[2]
            detect.height = detected_box[3]

        return resp


def run():
    model.load()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bytes2boxes_pb2_grpc.add_Bytes2BoxesServicer_to_server(
        Bytes2Boxes(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started image2boxes service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
