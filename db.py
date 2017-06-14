import logging
import os
import sqlite3 as sql
import sys


table_name = os.environ.get("SQLITE_TABLE")

try:
    con = sql.connect(os.environ.get("SQLITE_DB"))
    c = con.cursor()
    table_create = """
create table if not exists {0}(
channel text,
user_id text,
timestamp text,
message text
);""".format(table_name)
    c.execute(table_create)
except sql.Error as e:
    logging.error(e.args[0], exc_info=True)
    sys.exit(1)


def save_data(channel, user, content, date):
    logging.debug("channel:{0} user:{1} timestamp:{2} content:{3}",
                  channel, user, date, content)
    insert = """insert into {0} (channel, user_id, timestamp, message)
 values (?, ?, ?, ?)""".format(table_name)
    c.execute(insert, (channel, user, date, content))
    con.commit()
