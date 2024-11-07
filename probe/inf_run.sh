#!/bin/bash
# file: inf_run.sh
 
# run example:
# 	./inf_run.sh

VENV_DIR="venv"
. $VENV_DIR/bin/activate
echo "Virtual environment activated."

# Prompt user for the Python script directory
echo "PARAM FORMAT: collect.py nmp_ip  pcap_count ws" 
echo "PARAM FORMAT Ex.: collect.py http://0.0.0.0:25000 150 ws://1.1.1.1:30000" 
echo "nmp_ip (netsumap-core)" 
echo "pcap_count (Num packets to capture per run)"
echo "ws (Websocket server)" \n

read -p "Enter script params: " INF_PARAMS

/usr/bin/python3 collect.py $INF_PARAMS
