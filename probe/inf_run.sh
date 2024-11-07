#!/bin/bash
# file: inf_run.sh
 
# run example:
# 	./inf_run.sh

VENV_DIR="venv"
. $VENV_DIR/bin/activate
echo "Virtual environment activated."

# Prompt user for the Python script directory
echo "PARAM FORMAT: collect.py nmp_ip  pcap_count" 
echo "PARAM FORMAT Ex.: collect.py http://0.0.0.0:30000 150" 
echo "nmp_ip (netsumap-core IP/Hostname:Port)" 
echo "pcap_count (Num packets to capture per run)" \n

read -p "Enter script params: " INF_PARAMS

/usr/bin/python3 collect.py $INF_PARAMS
