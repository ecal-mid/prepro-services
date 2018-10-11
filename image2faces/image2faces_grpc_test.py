from __future__ import print_function

import argparse
import grpc

from protos import image2faces_pb2
from protos import image2faces_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default='test.jpeg', help='Input file')
parser.add_argument(
    '-r', '--rpc_url', default='35.204.2.242:50051', help='RPC url')
args = parser.parse_args()


def run():
    channel = grpc.insecure_channel(args.rpc_url)
    stub = image2faces_pb2_grpc.Image2FacesStub(channel)
    with open(args.input, "rb") as f:
        img_bytes = f.read()
        req = image2faces_pb2.Image2FacesRequest(input=img_bytes)
        response = stub.Run(req)
        print(response)


if __name__ == "__main__":
    run()
