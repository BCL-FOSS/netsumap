#!/bin/bash

sudo apt-get update -y
sudo apt-get upgrade -y

# Add Docker's official GPG key:
sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y 

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo docker build -t netsumap-dashboard .

sudo docker network create nmp-net

# Start netsumap container and web app
sudo docker run --gpus all --name netsumap --network nmp-net \
  --publish 30000:3000 -d -it -v $(pwd):$(pwd) -w $(pwd) docker.io/library/netsumap-dashboard

sudo docker exec -it netsumap bash -c 'hypercorn app:app --bind 0.0.0.0:3000'

