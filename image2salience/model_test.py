import tensorflow as tf
import numpy as np
import os
from scipy import misc
import argparse

import model

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,
    help='input image', default = 'test_img.jpg')
parser.add_argument('--model_path', type=str,
    help='model meta graph',
    default = 'Salient-Object-Detection/meta_graph/my-model.meta')
parser.add_argument('--checkpoint_path', type=str,
    help='model checkpoint',
    default = 'Salient-Object-Detection/salience_model_v1')
args = parser.parse_args()

def run():
    model.load(args.model_path, args.checkpoint_path)
    rgb = misc.imread(args.input)
    print(rgb)
    result = model.run(rgb)
    misc.imsave('model_test_result.png', result)


if __name__ == '__main__':
    run()
