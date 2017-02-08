#/usr/bin/env python3

# This has the rethink connection stuff.

import rethinkdb as r
import os

DB_NAME = "agile_youth"

def connect():
    """Return a rethinkdb connection"""
    RDB_HOST =  os.environ.get('RDB_HOST') or 'localhost'
    RDB_PORT = os.environ.get('RDB_PORT') or 28015
    return r.connect(host=RDB_HOST, port=RDB_PORT, db=DB_NAME)

def setup():
    cn = connect()
    
    def mktable(name):
        if name not in r.table_list().run(cn):
            r.table_create(name).run(cn)

    if DB_NAME not in r.db_list().run(cn):
        r.db_create(DB_NAME).run(cn)
    
    mktable("test")

r = r
