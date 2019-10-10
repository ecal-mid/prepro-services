from __future__ import print_function

import argparse
import base64
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='test_img.jpg', help='Input file')
parser.add_argument('--url', default='http://127.0.0.1:5001/run', help='Server url')
args = parser.parse_args()


def run():
    with open(args.input, "rb") as f:
        data = f.read()
        r = requests.post(args.url, data=data)
        with open('image2salience_http_result.png', 'wb') as of:
            of.write(r.content)

if __name__ == "__main__":
    run()
