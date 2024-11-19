#!/bin/bash
# file: inf_init.sh
 
# run example:
# 	./inf_init.sh

sudo apt-get update -y
sudo apt-get upgrade -y

# Install necessary python libraries system wide for script access.
sudo apt-get install python3-scapy -y
sudo apt install python3-requests -y
sudo apt install python3-psutil -y

dot="$(cd "$(dirname "$0")"; pwd)"
script="$dot/inf_run.sh"

echo $script
# Check if script exists
if [ ! -f $script ]; then
    echo "Error: File does not exist"
    exit 1
fi

# Check if the cron job already exists
(sudo crontab -l | grep -F "$CRON_JOB") > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Cron job already exists. No changes made."
else
    # Prompt user for additional parameters
    echo "PARAM FORMAT Ex.:https://core-server-url.com 150" 
    echo "nmp_ip (netsumap-core url)" 
    echo "pcap_count (# packets to capture per run)"
    echo $script
    read -p "Enter Parameters: " SCRIPT_PARAMS

    # Construct the cron job command
    CRON_JOB="*/5 * * * * /usr/bin/python3 $script $SCRIPT_PARAMS"

    # Add the cron job
    (sudo crontab -l; echo "$CRON_JOB") | sudo crontab -

    echo "Cron job added to run the script every 5 minutes with parameters: $SCRIPT_PARAMS"
fi






