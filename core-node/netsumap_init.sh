#!/bin/bash

sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 6363

sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo apt install docker-compose -y

docker compose build --no-cache 

docker volume create --name=redis_data
docker volume create --name=caddy_data
docker volume create --name=caddy_config
docker volume create --name=quart_app_data

docker compose up -d

