#!/bin/bash
# file: inf_init.sh
 
# run example:
# 	./inf_init.sh

sudo apt-get update -y
sudo apt-get upgrade -y

# Install Scapy from ubuntu repos
sudo apt-get install python3-scapy -y

scriptdir= $(pwd)
scriptfile= "inf_run.sh"
findscript= $scriptdir$scriptfile
echo $findscript
# Check if script exists
if [ ! -f $findscript]; then
    echo "Error: File does not exist"
    exit 1
fi

sudo apt install python3.12-venv -y
python3 -m venv .venv
. .venv/bin/activate
pip install requests

# Prompt user for additional parameters
echo "PARAM FORMAT Ex.:http://0.0.0.0:25000 150" 
echo "nmp_ip (netsumap-core IP/Hostname:Port)" 
echo "pcap_count (Num packets to capture per run)"
echo $findscript
read -p "Enter Parameters: " SCRIPT_PARAMS

# Construct the cron job command
CRON_JOB="*/5 * * * * /usr/bin/python3 $findscript $SCRIPT_PARAMS"

# Check if the cron job already exists
(sudo crontab -l | grep -F "$CRON_JOB") > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Cron job already exists. No changes made."
else
    # Add the cron job
    (sudo crontab -l; echo "$CRON_JOB") | sudo crontab -
    echo "Cron job added to run the script every 5 minutes with parameters: $SCRIPT_PARAMS"
fi






