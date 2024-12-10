#!/bin/bash
# file: probe_init.sh
 
# run example:
# 	./probe_init.sh

sudo apt-get update -y
sudo apt-get upgrade -y

sudo ufw allow 6363
sudo ufw allow 5000

sudo apt-get install -y \
    iperf3\
    p0f\
    tshark -y

pip install --no-cache-dir -r requirements.txt --upgrade 

