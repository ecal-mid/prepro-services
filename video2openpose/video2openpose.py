from concurrent import futures

import argparse
import subprocess
import grpc
import time
import os
import json

from protos import bytes2text_pb2
from protos import bytes2text_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_MAX_MESSAGE_LENGTH = 200 * 1024 * 1024

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()


class Bytes2Text(bytes2text_pb2_grpc.Bytes2TextServicer):

    def Run(self, request, context):

        with open('/tmp/video.mov', 'wb') as vf:
            vf.write(request.input)

        print('Processing video..')

        result = subprocess.check_output([
            './build/examples/openpose/openpose.bin', '--display', '0',
            '--video', '/tmp/video.mov', '--write_json', '/tmp/output_json'
        ])

        print('Processing results..')

        jsons = os.listdir('/tmp/output_json')
        result_response = {}
        for j in jsons:
            frame_name = int(j.split('_')[1])
            result_response[frame_name] = json.load(
                open('/tmp/output_json/%s' % j))
        json_response = json.dumps(result_response, sort_keys=True, indent=2)

        print('Done.')
        return bytes2text_pb2.Bytes2TextReply(output=json_response)


def run():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[('grpc.max_send_message_length', _MAX_MESSAGE_LENGTH),
                 ('grpc.max_receive_message_length', _MAX_MESSAGE_LENGTH)])
    bytes2text_pb2_grpc.add_Bytes2TextServicer_to_server(Bytes2Text(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started video2openpose service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
