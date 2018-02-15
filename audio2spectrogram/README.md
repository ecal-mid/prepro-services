# Audio 2 Spectrogram

Exports a spectrogram png from a mono audio file
Each column of pixel represent a 60hz frame.

## How to run

Pull the image directly from docker hub
```
docker run --rm -p 50051:50051 kikko/audio2spectrogram
```

Or build the image locally
```
docker build -t audio2spectrogram .
docker run --rm -p 50051:50051 audio2spectrogram
```

## How to test

```
pip install grpcio
python audio2spectrogram --input=mono.wav --output=spectrogram.png
```
