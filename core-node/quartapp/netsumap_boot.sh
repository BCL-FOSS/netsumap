#!/bin/bash

hypercorn app:app --bind 0.0.0.0:5000 --log-level debug