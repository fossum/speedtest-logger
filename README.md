# Speedtest Logger

The Speedtest Logger is a simple container that periodically runs
a speed test from speedtest.net and logs the result to a MySQL
database. Most of it is configurable, but I'm sure there is room for
improvements. Feel free to log new issues and/or pull-requests.

## DockerHub

```
docker pull fossum/speedtest-logger
```

https://hub.docker.com/r/fossum/speedtest-logger

### List Available Servers

```
docker run --rm fossum/speedtest-logger list
```

### Configuring as a Service

**Without a swarm:**

```
docker run -d --env-file .env --name speedtest fossum/speedtest-logger
```

**With a swarm:**

```
docker service create --env-file .env --name speedtest fossum/speedtest-logger
```

### Environment Variables

#### MYSQL_SERVER

Hostname or IP of the MySQL server that already has a
configured database and user for this task. Optionally
the table can be preconfigured as well.

#### MYSQL_USER

MySQL user to create table and insert rows.

#### MYSQL_PASS

MySQL password for user account.

#### MYSQL_DATABASE

Preconfigured database for table and user.

#### MYSQL_TABLE

Name of table to use in the database. Defaults to "internet-speed".

#### TEST_SERVER_ID

Integer value representing a specific speedtest.net
server. These numbers can be found by running
`speedtest-cli --list`. With the Docker image, you can run
`docker run -it --rm --env-file .env fossum/speedtest-logger list`.

#### SLEEP_TIME

Time in minutes to sleep between tests. Defaults to 10.
