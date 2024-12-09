#!/bin/bash
# file: inf_unenroll.sh
 
# run example:
# 	./inf_unenroll.sh

dot="$(cd "$(dirname "$0")"; pwd)"
script="$dot/inf_run.sh"

# Construct the cron job command
CRON_JOB="*/5 * * * * /usr/bin/python3 $script $1 $2"

# Check if the cron job already exists
(sudo crontab -l | grep -F "$CRON_JOB") > /dev/null 2>&1

if [ $? -eq 0 ]; then
    sudo crontab -l | grep -v "$CRON_JOB"  | sudo crontab -
    echo "Cronjob deletion success"
else
    echo "Cronjob does not exist. No changes made"
fi