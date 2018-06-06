import argparse
import logging
import sys
import time

import cv2
import numpy as np

import sys
sys.path.insert(0, 'tf-pose-estimation')

from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

estimator = None
NUM_JOINTS = common.CocoPart.Background.value

logger = logging.getLogger('TfPoseEstimator')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def run(image, resize_out_ratio=4.0):

    t = time.time()

    humans = estimator.inference(
        image, resize_to_default=True, upsample_size=resize_out_ratio)

    elapsed = time.time() - t

    logger.info('inference imagein %.4f seconds.' % elapsed)

    return humans


def load(model='mobilenet_thin', resize='656x368'):
    w, h = model_wh(resize)
    global estimator
    if w == 0 or h == 0:
        estimator = TfPoseEstimator(
            get_graph_path(model), target_size=(432, 368))
    else:
        estimator = TfPoseEstimator(get_graph_path(model), target_size=(w, h))
