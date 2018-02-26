from concurrent import futures

import argparse
import numpy as np
import time
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

import grpc

import sys
sys.path.insert(0, 'protos')

from protos import frames2bytes_pb2
from protos import frames2bytes_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()


class Frames2Bytes(frames2bytes_pb2_grpc.Frames2BytesServicer):

    def Run(self, request, context):
        # Load frame A
        buff_a = BytesIO(request.frameA)
        img = Image.open(buff_a)
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)))
        img_a = np.array(img)
        frame_a = img_a[:, :, ::-1].copy()

        # Get HSV
        prvs = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
        hsv = np.zeros_like(frame_a)
        hsv[..., 1] = 255

        # Load frame B
        buff_b = BytesIO(request.frameB)
        img = Image.open(buff_b)
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)))
        img_b = np.array(img)
        frame_b = img_b[:, :, ::-1].copy()

        # Calc flow
        next = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5,
                                            1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        output = BytesIO()
        output.write(cv2.imencode('.png', bgr)[1])
        value = output.getvalue()
        output.close()
        return frames2bytes_pb2.Frames2BytesReply(output=value)


def run():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    frames2bytes_pb2_grpc.add_Frames2BytesServicer_to_server(
        Frames2Bytes(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started frames2flow service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
