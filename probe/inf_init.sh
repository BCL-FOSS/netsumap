#!/bin/bash
# file: inf_init.sh
 
# run example:
# 	./inf_init.sh

# Prompt user for the Python script directory
read -p "Enter the full path to your Python script: " PYTHON_SCRIPT

# Check if the file exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: File does not exist at $PYTHON_SCRIPT"
    exit 1
fi

# Prompt user for additional parameters
echo "PARAM FORMAT: collect.py nmp_ip  pcap_count ws" 
echo "PARAM FORMAT Ex.: collect.py http://0.0.0.0:25000 150 ws://1.1.1.1:30000" 
echo "nmp_ip (netsumap-core IP/Hostname:Port)" 
echo "pcap_count (Num packets to capture per run)"
echo "ws (Websocket server)" \n
read -p "Enter Parameters: " SCRIPT_PARAMS

# Construct the cron job command
CRON_JOB="*/5 * * * * /usr/bin/python3 $PYTHON_SCRIPT $SCRIPT_PARAMS"

# Check if the cron job already exists
(crontab -l | grep -F "$CRON_JOB") > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Cron job already exists. No changes made."
else
    # Add the cron job
    (crontab -l; echo "$CRON_JOB") | crontab -
    echo "Cron job added to run the script every 5 minutes with parameters: $SCRIPT_PARAMS"
fi






