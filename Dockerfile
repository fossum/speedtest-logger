
FROM ubuntu

RUN apt update && apt install --assume-yes speedtest-cli ca-certificates python3-pip cron

RUN /etc/init.d/cron stop

RUN python3 -m pip install mysql-connector

ADD main.py speedtest/main.py
ADD entrypoint.sh speedtest/entrypoint.sh

ENV MYSQL_SERVER='localhost'
ENV MYSQL_USER='mysql_user'
ENV MYSQL_PASS='mysql_pass'
ENV MYSQL_DATABASE='mysql_database'

ENV TEST_SERVER_ID='1'

ENTRYPOINT [ "/bin/bash", "/speedtest/entrypoint.sh" ]
