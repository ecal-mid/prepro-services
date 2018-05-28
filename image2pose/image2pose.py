from concurrent import futures

import argparse
import numpy as np
import time
from PIL import Image
from io import BytesIO

import grpc

import sys
sys.path.insert(0, 'protos')

import pose_pb2
import image2pose_pb2
import image2pose_pb2_grpc

import model

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()


class Image2Pose(image2pose_pb2_grpc.Image2PoseServicer):

    def Run(self, request, context):
        # Run detection
        buff = BytesIO(request.image)
        img = Image.open(buff)
        img_arr = np.array(img)
        img_arr_format = img_arr[:, :, ::-1].copy()
        results = model.run(img_arr_format)

        # Send response
        resp = image2pose_pb2.Image2PoseReply()
        image_w, image_h = img.size
        centers = {}
        for human in results:
            pose = resp.result.poses.add()
            pose.id = -1
            pose.type = pose_pb2.POSE_TYPE_OPENPOSE_FULL
            for i in range(model.NUM_JOINTS):
                pt = pose.points.add()
                if i not in human.body_parts.keys():
                    continue
                pt.x = human.body_parts[i].x
                pt.y = human.body_parts[i].y

        return resp


def run():
    model.load()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image2pose_pb2_grpc.add_Image2PoseServicer_to_server(Image2Pose(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started image2pose service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
