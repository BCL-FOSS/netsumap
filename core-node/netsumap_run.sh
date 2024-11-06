#!/bin/bash

# Stop image
sudo docker stop netsumap-tensorflow
sudo docker rm netsumap-tensorflow

# Restart image
sudo docker run --gpus all --name netsumap -d -it -v $(pwd):$(pwd) -w $(pwd) docker.io/library/netsumap-tensorflow

sudo docker exec -it netsumap bash -c 'hypercorn app:app --bind 0.0.0.0:25000'