#!/bin/bash
# file: inf_init.sh
 
# run example:
# 	./inf_init.sh

sudo apt-get update -y
sudo apt-get upgrade -y

# Install Scapy from ubuntu repos
sudo apt-get install -y \
    python3-scapy \
    python3-Flask \
    python3-hypercorn \
    python3-scapy \
    python3-requests \
    python3-psutil \
    python3-iperf3 \
    python3-pyshark

dot="$(cd "$(dirname "$0")"; pwd)"
script="$dot/inf_run.sh"

echo $script
# Check if script exists
if [ ! -f $script ]; then
    echo "Error: File does not exist"
    exit 1
fi

# sudo apt install python3.12-venv -y
# python3 -m venv .venv
# . .venv/bin/activate
# pip install --no-cache-dir -r requirements.txt --upgrade 

# Prompt user for additional parameters
echo "PARAM FORMAT Ex.:https://netsumap-core-url" 

echo $script
read -p "Enter Parameters: " SCRIPT_PARAMS

# Construct the cron job command
CRON_JOB="*/5 * * * * /usr/bin/python3 $script $SCRIPT_PARAMS"

# Check if the cron job already exists
(sudo crontab -l | grep -F "$CRON_JOB") > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Cron job already exists. No changes made."
else
    # Add the cron job
    (sudo crontab -l; echo "$CRON_JOB") | sudo crontab -

    echo "Cron job added to run the script every 5 minutes with parameters: $SCRIPT_PARAMS"
fi