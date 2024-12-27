#!/bin/bash
# file: prb_conf.sh
 
# run example:
# 	./prb_conf.sh

wrkdir="$(cd "$(dirname "$0")"; pwd)"
script="$wrkdir/prb_run.sh"

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