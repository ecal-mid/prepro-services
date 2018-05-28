from __future__ import print_function

import argparse
import grpc

import sys
sys.path.insert(0, 'protos')

# import pose_pb2
import image2pose_pb2
import image2pose_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i',
    '--input',
    default='tf-pose-estimation/images/p3_dance.png',
    help='Input file')
parser.add_argument(
    '-r', '--rpc_url', default='localhost:50051', help='RPC url')
args = parser.parse_args()


def run():
    channel = grpc.insecure_channel(args.rpc_url)
    stub = image2pose_pb2_grpc.Image2PoseStub(channel)
    with open(args.input, "rb") as f:
        img_bytes = f.read()
        req = image2pose_pb2.Image2PoseRequest(image=img_bytes)
        response = stub.Run(req)
        print(response.result)


if __name__ == "__main__":
    run()
