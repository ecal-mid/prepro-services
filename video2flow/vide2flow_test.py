from __future__ import print_function

import argparse
import grpc

from protos import bytes2bytes_pb2
from protos import bytes2bytes_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i', '--input', default='_test_data/video_micro.mov', help='Input file')
parser.add_argument(
    '-o', '--output', default='_test_data/frames.zip', help='Output file')
parser.add_argument(
    '-r', '--rpc_url', default='localhost:50051', help='RPC url')
args = parser.parse_args()


def run():
    channel = grpc.insecure_channel(args.rpc_url)
    stub = bytes2bytes_pb2_grpc.Bytes2BytesStub(channel)
    with open(args.input, "r") as f:
        content = f.read()
        response = stub.Run(bytes2bytes_pb2.Bytes2BytesRequest(input=content))
        print(response.output)
        with open(args.output, 'w') as fo:
            fo.write(response.output)


if __name__ == "__main__":
    run()
