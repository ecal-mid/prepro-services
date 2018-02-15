## prepro-services
cyril.diagne [at] ecal.ch

Repository of services for the video preprocessing pipeline of the spring creative coding course at ECAL M&ID Bachelor.

Each service is configured and designed to be accessible through a kubernetes cluster via docker containers.

*Note:* `video2frames` and `video2audio` will be run from the client directly.
The reason is that ffmpeg is broadly available and easy to install whereas video2<x> prepros are bandwidth intensive.
