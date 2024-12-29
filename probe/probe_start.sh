#!/bin/bash

sudo nohup hypercorn app:app --bind 0.0.0.0:5000 >> probe_log.txt 2>&1 &

#sudo hypercorn app:app --bind 0.0.0.0:5000
