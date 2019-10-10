import base64
import os
import json
from flask import Flask, jsonify, request, Response
from io import BytesIO
from PIL import Image
import numpy as np
import logging
import model

model_path = 'Salient-Object-Detection/meta_graph/my-model.meta'
checkpoint_path = 'Salient-Object-Detection/salience_model_v1'
model.load(model_path, checkpoint_path)

def image_to_numpy(data):
    buff = BytesIO(data)
    img = Image.open(buff)
    return np.array(img)

def np_image_to_png(data):
    output = BytesIO()
    img = Image.fromarray(data.astype('uint8'), mode='L')
    img.save(output, format="PNG")
    value = output.getvalue()
    output.close()
    return value

# SERVER

app = Flask(__name__)

@app.route('/check', methods=['GET'])
def check():
    """Check"""
    return "Live"


@app.route('/run', methods=['POST'])
def run():
    original_image = request.get_data()
    np_arr = image_to_numpy(original_image)
    result = model.run(np_arr)
    salience_image = np_image_to_png(result)
    return Response(salience_image, mimetype='image/png')


# error handles
@app.errorhandler(404)
def page_not_found(_):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5001, debug=True)