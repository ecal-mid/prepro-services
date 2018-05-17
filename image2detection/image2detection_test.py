from __future__ import print_function

import argparse
import grpc

from protos import bytes2boxes_pb2
from protos import bytes2boxes_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i', '--input', default='../_test_data/test.png', help='Input file')
parser.add_argument(
    '-r', '--rpc_url', default='localhost:50051', help='RPC url')
args = parser.parse_args()


def run():
    channel = grpc.insecure_channel(args.rpc_url)
    stub = bytes2boxes_pb2_grpc.Bytes2BoxesStub(channel)
    with open(args.input, "rb") as f:
        img_bytes = f.read()
        req = bytes2boxes_pb2.Bytes2BoxesRequest(input=img_bytes)
        response = stub.Run(req)
        print(response.detections)


if __name__ == "__main__":
    run()
