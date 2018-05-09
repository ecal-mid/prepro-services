from concurrent import futures

import argparse
import numpy as np
import time
from PIL import Image
import tensorflow as tf
from io import BytesIO

import grpc

from protos import bytes2bytes_pb2
from protos import bytes2bytes_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()

import sys
sys.path.insert(0, 'FCRN_DepthPrediction')
sys.path.insert(0, 'protos')

import FCRN_DepthPrediction as models

net = None
sess = None
input_node = None

height = 228
width = 304
channels = 3
batch_size = 1


class Bytes2Bytes(bytes2bytes_pb2_grpc.Bytes2BytesServicer):

    def Run(self, request, context):
        # Prepare input image
        buff = BytesIO(request.input)
        img = Image.open(buff)
        img = img.resize([width, height], Image.ANTIALIAS)
        img = np.array(img).astype('float32')
        img = np.expand_dims(np.asarray(img), axis=0)
        # Run detection
        pred = sess.run(net.get_output(), feed_dict={input_node: img})
        # Save output
        output = BytesIO()
        img = Image.fromarray(pred[0, :, :, 0] * 25).convert('RGB')
        img.save(output, format="PNG")
        value = output.getvalue()
        output.close()
        # Return result
        return bytes2bytes_pb2.Bytes2BytesReply(output=value)


def run():
    # Create a placeholder for the input image
    global input_node
    input_node = tf.placeholder(
        tf.float32, shape=(None, height, width, channels))
    # Construct the network
    global net
    net = models.ResNet50UpProj({'data': input_node}, batch_size, 1, False)
    global sess
    sess = tf.Session()
    saver = tf.train.Saver()
    saver.restore(sess, 'FCRN_DepthPrediction/checkpoint/NYU_FCRN.ckpt')

    # Start server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bytes2bytes_pb2_grpc.add_Bytes2BytesServicer_to_server(
        Bytes2Bytes(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started image2depth service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
