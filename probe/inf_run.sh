#!/bin/bash
# file: inf_run.sh
 
# run example:
# 	./inf_run.sh

scriptdir= $(pwd)
scriptfile= "collect.py"
findscript= $scriptdir$scriptfile
# Check if script exists
if [ ! -f $findscript]; then
    echo "Error: File does not exist"
    exit 1
fi

# Prompt user for the Python script directory
echo "PARAM FORMAT Ex.:http://0.0.0.0:25000 150" 
echo "nmp_ip (netsumap-core IP/Hostname:Port)" 
echo "pcap_count (Num packets to capture per run)"\n

read -p "Enter script params: " INF_PARAMS

# Start venv
. .venv/bin/activate 

# Run collector.py
/usr/bin/python3 $findscript $INF_PARAMS
