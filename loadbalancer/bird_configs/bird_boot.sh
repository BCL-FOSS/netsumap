#!/bin/bash

#Setup BGP interface w/ reserved IP
sudo ip link add dev bird_link type dummy
sudo ip link set bird_link up
sudo ip addr add dev bird_link 45.32.65.235/32 #Reserved IP
sudo ip addr show dev bird_link