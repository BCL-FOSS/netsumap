#!/bin/bash

enroll() {
    if [ -f $ENROLL_SCRIPT ]; then
        sudo chmod +x $ENROLL_SCRIPT
        sudo source $ENROLL_SCRIPT
    else
        echo "Error: Enroll script not found at $ENROLL_SCRIPT"
        exit 1
    fi
}

unenroll() {
    if [ -f $UNENROLL_SCRIPT ]; then
        sudo chmod +x $UNENROLL_SCRIPT
        sudo source $UNENROLL_SCRIPT
    else
        echo "Error: Unenroll script not found at $UNENROLL_SCRIPT"
        exit 1
    fi
}

# Main
WRKDIR="$(cd "$(dirname "$0")"; pwd)"

echo $WRKDIR

PRB_CFG_DIR="$WRKDIR/config"

ENROLL_SCRIPT="$PRB_CFG_DIR/enroll.sh"
UNENROLL_SCRIPT="$PRB_CFG_DIR/unenroll.sh"

if [ "$1" == "enroll" ]; then
    enroll
elif [ "$1" == "unenroll" ]; then
    unenroll
else
    echo "Usage: $0 [enroll | unenroll]"
    exit 1
fi