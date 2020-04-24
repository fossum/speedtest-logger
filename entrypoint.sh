#!/bin/bash

# Exit when any command fails.
set -e

# If asking for list. Print list and exit.
if [[ "$1" == "list" ]] ; then
    speedtest-cli --list | head -n 20
    exit 0
fi

# Print SpeedTest Logger header.
echo "*********************************"
echo "SpeedTest Logger has been started"
echo "*********************************"

# Else, run the logger loop.
while true; do
    python3 /speedtest/main.py
    # Wait for some delay period (converted to minutes).
    sleep $(($SLEEP_TIME * 60))
done
