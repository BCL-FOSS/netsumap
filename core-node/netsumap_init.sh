#!/bin/bash

sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo apt install docker-compose

docker volume create netsumap_caddy_data

docker-compose build --no-cache && docker-compose up

