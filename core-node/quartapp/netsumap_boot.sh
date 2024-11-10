#!/bin/bash

. venv/bin/activate

hypercorn app:app --bind 0.0.0.0:5000