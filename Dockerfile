
FROM ubuntu

# Install the required software.
RUN apt update && apt install --assume-yes speedtest-cli ca-certificates python3-pip
RUN python3 -m pip install mysql-connector

# Add the needed scripts.
ADD main.py speedtest/main.py
ADD entrypoint.sh speedtest/entrypoint.sh

# Some default information that wont work 
# without overrides (see README).
ENV MYSQL_SERVER='localhost'
ENV MYSQL_USER='mysql_user'
ENV MYSQL_PASS='mysql_pass'
ENV MYSQL_DATABASE='mysql_database'
ENV TEST_SERVER_ID='1'

# Every 10 minutes.
ENV SLEEP_TIME 10

# By default, run the entry script.
ENTRYPOINT [ "/bin/bash", "/speedtest/entrypoint.sh" ]
