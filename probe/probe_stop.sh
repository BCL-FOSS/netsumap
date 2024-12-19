#!/bin/bash

# Find the process ID (PID) of the Hypercorn application
pid=$(ps aux | grep 'hypercorn app:app --bind 0.0.0.0:5000' | grep -v grep | awk '{print $2}')

# Check if the PID exists
if [ -n "$pid" ]; then
    echo "Stopping Hypercorn application with PID: $pid"
    sudo kill "$pid"
    if [ $? -eq 0 ]; then
        echo "Hypercorn application stopped successfully."
    else
        echo "Failed to stop Hypercorn application."
    fi
else
    echo "No running Hypercorn application found."
fi
