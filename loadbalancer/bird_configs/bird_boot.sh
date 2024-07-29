#!/bin/bash

#Setup BGP interface w/ reserved IP
ip link add dev bird_link type dummy
ip link set bird_link up
ip addr add dev bird_link 45.76.27.93/32 #Reserved IP
ip addr show dev bird_link