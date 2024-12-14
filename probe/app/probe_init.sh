#!/bin/bash
# file: probe_init.sh
 
# run example:
# 	./probe_init.sh

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install -y \
    iperf3\
    p0f\
    tshark -y