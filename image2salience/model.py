import tensorflow as tf
import numpy as np
import os
from scipy import misc

g_mean = np.array(([126.88,120.24,112.19])).reshape([1,1,3])
session = None
image_batch = None
pred_mattes = None

def rgba2rgb(img):
	return img[:,:,:3] * np.expand_dims(img[:,:,3], 2)

def load(model_path, checkpoint_path):
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = 0.8)
    global session
    session = tf.Session(config=tf.ConfigProto(gpu_options = gpu_options))

    saver = tf.train.import_meta_graph(model_path)
    saver.restore(session, tf.train.latest_checkpoint(checkpoint_path))
    global image_batch
    image_batch = tf.get_collection('image_batch')[0]
    global pred_mattes
    pred_mattes = tf.get_collection('mask')[0]

def run(img):
    if img.shape[2] == 4:
        img = rgba2rgb(img)
    origin_shape = img.shape[:2]
    rescale = misc.imresize(img.astype(np.uint8), [320,320,3], interp="nearest")
    img = np.expand_dims(rescale.astype(np.float32) - g_mean, 0)

    pred_alpha = session.run(pred_mattes, feed_dict = {image_batch: img})
    final_alpha = misc.imresize(np.squeeze(pred_alpha), origin_shape)
    return final_alpha
    # misc.imsave(os.path.join(output_folder, 'alpha.png'), final_alpha)
