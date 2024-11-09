#!/bin/bash
# file: inf_unenroll.sh
 
# run example:
# 	./inf_unenroll.sh

dot="$(cd "$(dirname "$0")"; pwd)"
script="$dot/inf_run.sh"

if sudo crontab -l | grep -v "$script"  | sudo crontab - < "$0"; then
    echo "Cronjob deletion success"
else
    echo "Cronjob deletion failed"
    exit 1
fi