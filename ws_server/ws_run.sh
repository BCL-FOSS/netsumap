#!/bin/bash
# file: ws_run.sh
 
# run example:
# 	./ws_run.sh

sudo docker network disconnect ws-net ws-server
sudo docker stop ws-server
sudo docker rm ws-server

sudo docker run --name ws-server --network ws-net \
  --publish 30000:3000 -d -it -v $(pwd):$(pwd) -w $(pwd) docker.io/library/ws-server

sudo docker exec -it ws-server bash -c 'hypercorn app:app --bind 0.0.0.0:3000'

