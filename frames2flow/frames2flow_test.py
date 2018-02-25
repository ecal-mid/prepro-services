from __future__ import print_function

import argparse
import grpc

from protos import frames2bytes_pb2
from protos import frames2bytes_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument(
    '-iA', '--inputA', default='frameA.png', help='Input file A')
parser.add_argument(
    '-iB', '--inputB', default='frameB.png', help='Input file B')
parser.add_argument('-o', '--output', default='result.png', help='Output file')
parser.add_argument(
    '-r', '--rpc_url', default='localhost:50051', help='RPC url')
args = parser.parse_args()


def run():
    channel = grpc.insecure_channel(args.rpc_url)
    stub = frames2bytes_pb2_grpc.Frames2BytesStub(channel)
    with open(args.inputA, 'rb') as fA:
        with open(args.inputB, 'rb') as fB:
            a = fA.read()
            b = fB.read()

            response = stub.Run(
                frames2bytes_pb2.Frames2BytesRequest(frameA=a, frameB=b))
            with open(args.output, 'wb') as fo:
                fo.write(response.output)


if __name__ == "__main__":
    run()
