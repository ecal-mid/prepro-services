import base64
import numpy as np
from scipy import misc

import tensorflow as tf

import sys
sys.path.insert(0, 'facenet-master/src')
import facenet
import align.detect_face

pnet = None
rnet = None
onet = None

facenet_session = None
images_placeholder = None
embeddings = None
phase_train_placeholder = None


def load(pretrained_model_path):
    # Load face detection model
    facedetect_graph = tf.Graph()
    with facedetect_graph.as_default():
        facedetect_session = tf.Session()
        global pnet, rnet, onet
        pnet, rnet, onet = align.detect_face.create_mtcnn(
            facedetect_session, None)
    # Load Facenet Graph
    facenet_graph = tf.Graph()
    with facenet_graph.as_default():
        global facenet_session
        facenet_session = tf.Session()
        with facenet_session.as_default():
            facenet.load_model(pretrained_model_path)
            # Get input and output tensors
            global images_placeholder, embeddings, phase_train_placeholder
            images_placeholder = facenet_graph.get_tensor_by_name("input:0")
            embeddings = facenet_graph.get_tensor_by_name("embeddings:0")
            phase_train_placeholder = facenet_graph.get_tensor_by_name(
                "phase_train:0")


def run(img):
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    margin = 44
    image_size = 160

    img_size = np.asarray(img.shape)[0:2]
    bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet,
                                                      onet, threshold, factor)
    result = []
    if len(bounding_boxes) > 0:
        w = img.shape[1]
        h = img.shape[0]
        for bbox in bounding_boxes:
            ## det = np.squeeze(bounding_boxes[0,0:4])
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(bbox[0] - margin / 2, 0)
            bb[1] = np.maximum(bbox[1] - margin / 2, 0)
            bb[2] = np.minimum(bbox[2] + margin / 2, img_size[1])
            bb[3] = np.minimum(bbox[3] + margin / 2, img_size[0])
            cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
            aligned = misc.imresize(
                cropped, (image_size, image_size), interp='bilinear')
            prewhitened = facenet.prewhiten(aligned)

            feed_dict = {
                images_placeholder: [prewhitened],
                phase_train_placeholder: False
            }
            features = facenet_session.run(embeddings, feed_dict=feed_dict)
            # Save
            x1 = bbox[0] / w
            y1 = bbox[1] / h
            x2 = bbox[2] / w
            y2 = bbox[3] / h
            result.append([x1, y1, x2, y2, features[0]])
    return result
