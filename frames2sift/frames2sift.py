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

from protos import frames2sift_pb2
from protos import frames2sift_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# FLANN matcher
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params, search_params)


def get_matches(frame_a, frame_b):

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(frame_a, None)
    kp2, des2 = sift.detectAndCompute(frame_b, None)

    matches = []

    if len(kp2) and len(kp1):
        # get matches
        try:
            matches = flann.knnMatch(des1, des2, k=2)
            # ratio test as per Lowe's paper
            matches = [m for (m, n) in matches if m.distance < 0.7 * n.distance]
        except Exception:
            print('could not match keypoints')

    return {'kp1': kp1, 'kp2': kp2, 'matches': matches}


class Frames2Sift(frames2sift_pb2_grpc.Frames2SiftServicer):

    def Run(self, request, context):
        t1 = time.time()
        # Load frame A
        buff_a = BytesIO(request.frameA)
        img = Image.open(buff_a)
        img_a = np.array(img)
        frame_a = img_a[:, :, ::-1].copy()

        # Load frame B
        buff_b = BytesIO(request.frameB)
        img = Image.open(buff_b)
        img_b = np.array(img)
        frame_b = img_b[:, :, ::-1].copy()

        t2 = time.time()

        # Get keypoints & matches
        result = get_matches(frame_a, frame_b)

        t3 = time.time()

        # Build proto response.
        resp = frames2sift_pb2.Frames2SiftReply()
        for kp in result['kp1']:
            pt = resp.keypointsA.add()
            pt.x = kp.pt[0]
            pt.y = kp.pt[1]
        for kp in result['kp2']:
            pt = resp.keypointsB.add()
            pt.x = kp.pt[0]
            pt.y = kp.pt[1]
        for m in result['matches']:
            if hasattr(m, 'queryIdx'):
                mp = resp.matches.add()
                mp.keypointA = m.queryIdx
                mp.keypointB = m.trainIdx
                mp.distance = m.distance
        print('load: %.2fs, compute: %.2fs, total: %.2fs' % (
            (t2 - t1), (t3 - t2), (time.time() - t1)))
        return resp


def run():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    frames2sift_pb2_grpc.add_Frames2SiftServicer_to_server(
        Frames2Sift(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started frames2sift service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
