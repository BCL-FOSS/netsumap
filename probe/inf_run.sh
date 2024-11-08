#!/bin/bash
# file: inf_run.sh
 
# run example:
# 	./inf_run.sh

# Prompt user for the Python script directory
echo "PARAM FORMAT Ex.:http://0.0.0.0:25000 150" 
echo "nmp_ip (netsumap-core IP/Hostname:Port)" 
echo "pcap_count (Num packets to capture per run)"\n

read -p "Enter script params: " INF_PARAMS

# Start venv
. .venv/bin/activate 


/usr/bin/python3 collect.py $INF_PARAMS
