from __future__ import print_function

import argparse
import grpc

from google.protobuf.json_format import MessageToJson

from protos import frames2sift_pb2
from protos import frames2sift_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument(
    '-iA', '--inputA', default='frameA.png', help='Input file A')
parser.add_argument(
    '-iB', '--inputB', default='frameB.png', help='Input file B')
parser.add_argument(
    '-r', '--rpc_url', default='localhost:50051', help='RPC url')
args = parser.parse_args()

input_path = '/Users/cyril.diagne/Projets/2017-2018/creative-coding/prepro-js/examples/_data/test_video_small_new/prepros/frames'
output_path = '/Users/cyril.diagne/Projets/2017-2018/creative-coding/prepro-js/examples/_data/test_video_small_new/prepros/frames'

channel = grpc.insecure_channel(args.rpc_url)
stub = frames2sift_pb2_grpc.Frames2SiftStub(channel)


def track(a, b):
    response = stub.Run(frames2sift_pb2.Frames2SiftRequest(frameA=a, frameB=b))
    return MessageToJson(response)


def run_all():
    for i in range(1, 276):
        frame_a = input_path + '/frame-%03d.png' % i
        frame_b = input_path + '/frame-%03d.png' % (i + 1)
        with open(frame_a, 'rb') as fA:
            with open(frame_b, 'rb') as fB:
                with open('test/frame-%03d.json' % i, 'w') as of:
                    of.write(track(fA.read(), fB.read()))


def run():
    with open(args.inputA, 'rb') as fA:
        with open(args.inputA, 'rb') as fB:
            with open('result.json', 'w') as of:
                of.write(track(fA.read(), fB.read()))


if __name__ == "__main__":
    run()
