import logging
import os
import psycopg2 as sql
import sys


table_name = os.environ.get("DB_TABLE")

try:
    con = sql.connect(host=os.environ.get("DB_HOST"),
                      database=os.environ.get("DB_NAME"),
                      user=os.environ.get("DB_USER"),
                      password=os.environ.get("DB_PASSWORD"))
    c = con.cursor()
    table_create = """
create table if not exists {0}(
channel text,
user_id text,
timestamp timestamp,
message text
);""".format(table_name)
    c.execute(table_create)
    con.commit()
except sql.Error as e:
    logging.error(e.args[0], exc_info=True)
    sys.exit(1)


def save_data(channel, user, content, date):
    logging.debug("channel:{0} user:{1} timestamp:{2} content:{3}".format(
        channel, user, date, content))
    insert = """insert into {0} (channel, user_id, timestamp, message)
 values (%s, %s, to_timestamp(%s), %s)""".format(table_name)
    c.execute(insert, (channel, user, date, content))
    con.commit()
