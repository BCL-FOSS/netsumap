#!/bin/bash

# Stop Hypercorn process
sudo killall hypercorn

# Stop image
sudo docker network disconnect nmp-net netsumap
sudo docker stop netsumap
sudo docker rm netsumap

# Restart image
sudo docker run --gpus all --name netsumap --network nmp-net \
  --publish 30000:3000 -d -it -v $(pwd):$(pwd) -w $(pwd) docker.io/library/netsumap-dashboard

sudo docker exec -it netsumap bash -c 'hypercorn app:app --bind 0.0.0.0:3000'