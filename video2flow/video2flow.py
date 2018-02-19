from concurrent import futures

import argparse
import subprocess
import grpc
import time
import os
import json
import shutil
import flowviz
from PIL import Image

from protos import bytes2bytes_pb2
from protos import bytes2bytes_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=50051, help='GRPC port')
args = parser.parse_args()


class Bytes2Bytes(bytes2bytes_pb2_grpc.Bytes2BytesServicer):

    def Run(self, request, context):

        tmp_file = '_tmp_video.mov'
        tmp_frames_folder = '/tmp/_tmp_frames'
        tmp_flow_folder = '/tmp/_tmp_flow'

        with open(tmp_file, 'wb') as vf:
            vf.write(request.input)

        if not os.path.exists(tmp_frames_folder):
            os.mkdir(tmp_frames_folder)

        print('Extracting frames..')

        framerate = subprocess.check_output([
            'ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', 'V:0',
            '-show_entries', 'stream=r_frame_rate', tmp_file
        ])

        print(framerate)

        output = subprocess.check_output([
            'ffmpeg', '-i', tmp_file, '-v', '0', '-r', framerate, os.path.join(
                tmp_frames_folder, 'frame-%03d.png')
        ])

        result = subprocess.check_output([
            'python',
            'flownet2-pytorch/main.py',
            '--inference',
            '-nw',
            '1',
            '--model',
            'FlowNet2',
            '--inference_dataset',
            'ImagesFromFolder',
            '--inference_dataset_root',
            tmp_frames_folder,
            '--resume',
            'FlowNet2_checkpoint.pth.tar',
            '--save_flow',
            '--save',
            tmp_flow_folder,
        ])

        frames_folder = os.path.join(tmp_flow_folder, 'inference',
                                     'run.epoch-0-flow-field')
        files = os.listdir(frames_folder)

        tmp_viz_folder = '/tmp/flow_viz'

        if not os.path.exists(tmp_viz_folder):
            os.mkdir(tmp_viz_folder)

        for f in files:
            flow = flowviz.read_flow(os.path.join(frames_folder, f))
            img_array = flowviz.flow_to_image(flow)
            img = Image.fromarray(img_array)
            img.save(os.path.join(tmp_viz_folder, f.split('.')[0] + '.png'))

        #video = subprocess.check_output([
        #    'ffmpeg',
        #    '-i',
        #    os.path.join(tmp_viz_folder, '%06d.png',
        #    '-c:v',
        #    'libx264',
        #    '-pix_fmt',
        #    'yuv420p',
        #i])

        tmp_zip_file = '/tmp/flow.zip'

        print('Compressing results..')
        result = subprocess.check_output(
            ['zip', '-r', tmp_zip_file, tmp_viz_folder])

        shutil.rmtree(tmp_viz_folder)
        shutil.rmtree(tmp_flow_folder)
        shutil.rmtree(tmp_frames_folder)

        with open(tmp_zip_file, 'rb') as resfile:
            print('Done.')
            return bytes2bytes_pb2.Bytes2BytesReply(output=resfile.read())


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bytes2bytes_pb2_grpc.add_Bytes2BytesServicer_to_server(
        Bytes2Bytes(), server)
    server.add_insecure_port('[::]:%i' % args.port)
    server.start()
    print('started video2flow service on port %i' % args.port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()
