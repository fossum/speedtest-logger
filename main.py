"""Log internet speed test to a specified MySQL database.

Description:
    Designed for a Docker container, but could be used stand-alone.
    This script does a single speed test and logs it to the MySQL
    server defined by environmental variables.

Environment Variables:
    MYSQL_SERVER:
        Hostname or IP of the MySQL server that already has a
        configured database and user for this task. Optionally
        the table can be preconfigured as well.
    MYSQL_USER: MySQL user to create table and insert rows.
    MYSQL_PASS: MySQL password for user account.
    MYSQL_DATABASE: Preconfigured database for table and user.
    MYSQL_TABLE: Name of table to use in the database.
    TEST_SERVER_ID:
        Integer value representing a specific speedtest.net
        server. These numbers can be found by running
        `speedtest-cli --list`. With the Docker image, you can run
        `docker run -it --rm --env-file .env fossum/speedtest-logger
        list`.
"""

import json
import mysql.connector
import subprocess
import os

# Get environment variables for configuration.
MYSQL_SERVER = os.getenv('MYSQL_SERVER', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'user')
MYSQL_PASS = os.getenv('MYSQL_PASS', 'pass')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'database')
MYSQL_TABLE = os.getenv('MYSQL_TABLE', 'internetspeed')

TEST_SERVER_ID = os.getenv('TEST_SERVER_ID', '1')

# Example JSON output.
# json_str = b'''{
#     "download": 88764203.40414993,
#     "upload": 3605429.64171305,
#     "ping": 20.718
# }\n
# '''
# Run secure(HTTPS) speed test using specified server and outputing JSON data.
json_str = subprocess.check_output(
    ['speedtest-cli', '--json', '--server', TEST_SERVER_ID, '--secure'])
try:
    result = json.loads(json_str)
except json.JSONDecodeError as err:
    print(json_str)
    raise err

if not result:
    raise ValueError("Did not find a result.")

keys = [
    "download",
    "upload",
    "ping"
]

for key in keys:
    if key not in result.keys():
        raise ValueError("Result missing {} key.".format(key))

db_conn = mysql.connector.connect(
    host=MYSQL_SERVER,
    user=MYSQL_USER,
    passwd=MYSQL_PASS,
    database=MYSQL_DATABASE
)
db_cursor = db_conn.cursor()

# Create table if it doesn't exist.
db_cursor.execute(
    "CREATE TABLE IF NOT EXISTS `{}`.`{}` ".format(MYSQL_DATABASE,
                                                   MYSQL_TABLE) +
    "(`down` FLOAT, " +
    "`up` FLOAT, " +
    "`ping` FLOAT, " +
    "`timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP, " +
    "`index` INT(0) AUTO_INCREMENT, " +
    "PRIMARY KEY (`index`))"
)

# Insert row into database.
sql = ("INSERT INTO `{}` ".format(MYSQL_TABLE) +
       "(down, up, ping) " +
       "VALUES (%s, %s, %s)")
val = (
    result.get("download"),
    result.get("upload"),
    result.get("ping")
)
db_cursor.execute(sql, val)
db_conn.commit()
