#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

# Setup a cron schedule
echo "*/10 * * * * python3 /speedtest/main.py > /dev/stdout 2>&1
# This extra line makes it a valid cron" > scheduler.txt

# If asking for list. Print list and exit.

crontab scheduler.txt
cron -f
