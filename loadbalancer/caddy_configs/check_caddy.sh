#!/bin/bash

# Check if caddy server is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 

if ! pgrep 'caddy' > /dev/null
then
    ./usr/local/bin/caddy_boot.sh
else
    exit 0
fi