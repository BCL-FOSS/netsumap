#!/bin/bash

remove_cronjob() {
    CRON_IDENTIFIER="$WRKDIR/ping.py"

    if (sudo crontab -l | grep -F "$CRON_IDENTIFIER") > /dev/null 2>&1; then
        sudo crontab -l | grep -v "$CRON_IDENTIFIER" | sudo crontab -
        echo "Cron job containing '$CRON_IDENTIFIER' has been removed successfully."
    else
        echo "No cron job containing '$CRON_IDENTIFIER' found. No changes made."
    fi
}

# Main
WRKDIR="$(cd "$(dirname "$0")"; pwd)"

echo $WRKDIR

remove_cronjob

python3 cfg.py --unenroll

