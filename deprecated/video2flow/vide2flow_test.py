from __future__ import print_function

import argparse
import grpc

from protos import bytes2bytes_pb2
from protos import bytes2bytes_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default='test.mov', help='Input file')
parser.add_argument('-o', '--output', default='frames.zip', help='Output file')
parser.add_argument(
    '-r', '--rpc_url', default='10.192.250.140:30003', help='RPC url')
args = parser.parse_args()

MAX_MESSAGE_LENGTH = 200 * 1024 * 1024


def run():
    channel = grpc.insecure_channel(
        args.rpc_url,
        options=[('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)])
    stub = bytes2bytes_pb2_grpc.Bytes2BytesStub(channel)
    with open(args.input, "r") as f:
        content = f.read()
        response = stub.Run(bytes2bytes_pb2.Bytes2BytesRequest(input=content))
        with open(args.output, 'w') as fo:
            fo.write(response.output)


if __name__ == "__main__":
    run()
