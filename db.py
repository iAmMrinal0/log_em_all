import os
import sqlite3 as sql
import sys


table_name = os.environ.get("SQLITE_TABLE")

try:
    con = sql.connect(os.environ.get("SQLITE_DB"))
    c = con.cursor()
    table_create = """
create table if not exists {0}(
user_id text,
date text,
message text
);""".format(table_name)
    c.execute(table_create)
except sql.Error as e:
    print("Error encountered:{0}".format(e.args[0]))
    sys.exit(1)


def save_data(user, content, date):
    insert = """insert into {0} (user_id, date, message)
 values (?, ?, ?)""".format(table_name)
    c.execute(insert, (user, date, content))
    con.commit()


def get_data(user):
    fetch = "select date, message from {0} where user_id=(?)".format(
        table_name)
    c.execute(fetch, (user,))
    result = c.fetchall()
    return result
