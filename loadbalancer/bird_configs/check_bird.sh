#!/bin/bash

# Checks if BIRD routing daemon is running
# -x flag only match processes whose name (or command line if -f is specified) exactly match the pattern. 

if ! pgrep 'bird' > /dev/null
then
    if systemctl restart bird | grep -q 'failed'; then
        n=0
        while [ $n -lt 10 ]
        do
            
        done
    fi
    exit 1
else
    exit 0
fi