from concurrent import futures

import argparse
import numpy as np
import time
import tensorflow as tf
from PIL import Image
from io import BytesIO

import grpc

from protos import bytes2features_pb2
from protos import bytes2features_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()

import sys
sys.path.insert(0, 'protos')

model = None
output_tensor = None


class Bytes2Features(bytes2features_pb2_grpc.Bytes2FeaturesServicer):

    def Run(self, request, context):
        # Run detection
        buff = BytesIO(request.input)
        img = Image.open(buff)
        img = img.resize((299, 299))
        img_data = np.asarray(img)
        result = sess.run(output_tensor, {'input:0': [img_data]})
        result = np.squeeze(result).tolist()
        resp = bytes2features_pb2.Bytes2FeaturesReply()
        resp.features.extend(result)
        return resp


def run():
    global model
    with open('model/inception_v3_2016_08_28_frozen.pb', 'rb') as graph_file:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(graph_file.read())
        tf.import_graph_def(graph_def, name='')

    global sess
    sess = tf.Session()
    global output_tensor
    # retrieve feature vector
    output_tensor = sess.graph.get_tensor_by_name(
        'InceptionV3/Logits/AvgPool_1a_8x8/AvgPool:0')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bytes2features_pb2_grpc.add_Bytes2FeaturesServicer_to_server(
        Bytes2Features(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started image2features service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
