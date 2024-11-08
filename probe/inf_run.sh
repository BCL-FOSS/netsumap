#!/bin/bash
# file: inf_run.sh
 
# run example:
# 	./inf_run.sh

read INF_PARAMS

# Start venv
. .venv/bin/activate 

/usr/bin/python3 collect.py $INF_PARAMS
