from __future__ import print_function

import argparse
import base64
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='test_img.jpg', help='Input file')
parser.add_argument('--url', default='http://35.192.125.173:5001/run', help='Server url')
args = parser.parse_args()


def run():
    with open(args.input, "rb") as f:
        img_bytes = f.read()
        data = base64.b64encode(img_bytes)
        r = requests.post(args.url, data=data)
        with open('image2salience_http_result.png', 'wb') as of:
            of.write(r.content)

if __name__ == "__main__":
    run()
