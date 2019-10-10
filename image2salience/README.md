# image2salience HTTP server

Computes salience masks using: https://github.com/Joker316701882/Salient-Object-Detection

First you must clone the model's repo:

```
git clone https://github.com/Joker316701882/Salient-Object-Detection
```

Then download the pretrained weights from [here](https://drive.google.com/drive/folders/0B6l9O8aWij8fUGtVNldUTXA4eHc) and put
the `salience_model_v1` folder in `/Salient-Object-Detection/`.

## 1 - Test model (via virtualenv):

a) setup virtualenv

```
virtualenv venv
source venv/bin/activate
pip install -r requirements_http.txt
```

b) Install Tensorflow (v1.x)

```
pip install tensorflow==1.14.0
```

c) run model

```
python model_test.py
```

## 2 - Test model in HTTP Server (via virtualenv):

a) setup virtualenv

b) start server

```
python image2salience_http.py
```

b) test server

```
python image2salience_http_test.py
```

## 3 - Test HTTP Server in Docker:

a) build docker image

```
docker build -t image2salience:0.1.0-http-gpu . -f deploy/gpu.http.Dockerfile
```

b) start docker image server

```
docker run --rm -p 5001:5001 image2salience:0.1.0-http-gpu
```

c) test docker image server

```
python image2salience_http_test.py
```

## 3 - Test Docker image in Kubernetest (via skaffold):

a) deploy image on dev cluster in dev mode

```
skaffold dev -f deploy/gpu.http.skaffold.yaml
```

b) test docker image server

```
python image2salience_http_test.py --url http://<ip_of_your_service>:5001/run
```
