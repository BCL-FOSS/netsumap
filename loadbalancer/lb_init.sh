#!/bin/bash

#Install Caddy Server
#caddy adapt
#caddy start
#caddy stop
#caddy reload
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

#Allowed Traffic - UFW
#sudo ufw allow 22
sudo ufw allow 443/tcp
sudo ufw allow 179/tcp

#Default Policies - UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing

#Logging enabled - UFW
sudo ufw logging on

#Setup BGP interface w/ reserved IP
ip link add dev bird_link type dummy
ip link set bird_link up
ip addr add dev bird_link 45.76.27.93/32 #Reserved IP
ip addr show dev bird_link

#Setup BIRD routing daemon
apt install bird

nano /etc/bird/bird.conf