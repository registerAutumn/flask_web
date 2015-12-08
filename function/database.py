#!/usr/bin/env python
# -*- encoding: utf-8

import sqlite3
import re

DB_NAME = "backend.db"

def doing_sql(sql, args):
    database = sqlite3.connect("./function/%s" % DB_NAME)
    cursor = database.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    if re.match(r"^select.+", sql.lower()) == None:
        database.commit()
    return result