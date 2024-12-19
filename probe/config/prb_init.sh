#!/bin/bash
# file: inf_init.sh
 
# run example:
# 	./inf_init.sh

sudo apt-get update -y
sudo apt-get upgrade -y

sudo ufw allow 5000

sudo apt-get install -y \
    iperf3\
    p0f\
    tshark -y

pip install --no-cache-dir -r requirements.txt --upgrade 

dot="$(cd "$(dirname "$0")"; pwd)"
script="$dot/prb_run.sh"

echo $script
# Check if script exists
if [ ! -f $script ]; then
    echo "Error: File does not exist"
    exit 1
fi

echo "PARAM FORMAT Ex.:https://netsumap-core-url"
echo "Do not add a trailing / to the url" 

echo $script
read -p "Enter Parameters: " SCRIPT_PARAMS

# uptime check cron job
CRON_JOB="*/5 * * * * /usr/bin/python3 $script $SCRIPT_PARAMS"

# verify if cron job exist
(sudo crontab -l | grep -F "$CRON_JOB") > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Cron job already exists. No changes made."
else
    # Add cron job
    (sudo crontab -l; echo "$CRON_JOB") | sudo crontab -

    echo "Cron job added to run the script every 5 minutes with parameters: $SCRIPT_PARAMS"
fi