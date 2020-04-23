"""
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
MYSQL_TABLE = os.getenv('MYSQL_TABLE', 'internet-speed')

TEST_SERVER_ID = os.getenv('TEST_SERVER_ID', '1')

# Example using Spokane CenturyLink server (id: 10166):
# root@47eab7b1d167:/# speedtest-cli --json --server 10166 --secure
# json_str = b'{"download": 88764203.40414993, "upload": 3605429.64171305, "ping": 20.718}\n'
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
    "CREATE TABLE IF NOT EXISTS `{}`.`{}` (`down` FLOAT, `up` FLOAT, `ping` FLOAT, `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, `index` INT(0) AUTO_INCREMENT, PRIMARY KEY (`index`))".format(MYSQL_DATABASE, MYSQL_TABLE)
)

# Insert row.
sql = "INSERT INTO `{}` (down, up, ping) VALUES (%s, %s, %s)".format(MYSQL_TABLE)
val = (
    result.get("download"),
    result.get("upload"),
    result.get("ping")
)
db_cursor.execute(sql, val)
db_conn.commit()

print(db_cursor.rowcount, "record inserted.")
