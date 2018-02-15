from concurrent import futures

import argparse
import numpy as np
import time
from PIL import Image
from scipy import signal
from scipy.io import wavfile
from io import BytesIO

import grpc

from protos import bytes2bytes_pb2
from protos import bytes2bytes_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--framerate', default=60, help='Framerate to export')
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()


class Bytes2Bytes(bytes2bytes_pb2_grpc.Bytes2BytesServicer):

    def Run(self, request, context):

        buff = BytesIO(request.input)
        sample_rate, samples = wavfile.read(buff)
        frequencies, times, spectogram = signal.spectrogram(
            samples, sample_rate)

        # convert to dB
        decibels = 10 * np.log10(1 + spectogram)

        norm = np.max(decibels)
        gray = decibels / norm * 255
        im = Image.fromarray(gray).convert('L')

        duration = float(len(samples)) / sample_rate
        im = im.resize((int(duration * args.framerate), gray.shape[0]))
        output = BytesIO()
        im.save(output, format="PNG")
        value = output.getvalue()
        output.close()
        return bytes2bytes_pb2.Bytes2BytesReply(output=value)


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bytes2bytes_pb2_grpc.add_Bytes2BytesServicer_to_server(
        Bytes2Bytes(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started audio2spectrogram service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
