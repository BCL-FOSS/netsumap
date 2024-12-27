#!/bin/bash
# file: prb_enroll.sh
 
# run example:
# 	./prb_enroll.sh

sudo apt-get update -y
sudo apt-get upgrade -y

sudo ufw allow 5000

sudo apt-get install -y \
    iperf3\
    p0f\
    tshark -y

pip install --no-cache-dir -r requirements.txt --upgrade 

/usr/bin/python3 probe_conf.py $1