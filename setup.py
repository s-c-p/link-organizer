#!/usr/bin/env python3

"""
runs everytime a new user is created
TODO: create a ``unSetup.py``
"""

import sqlite3

USER_FILE = "1655df96-89f1-494c-955a-25758a93e104"

with sqlite3.connect(USER_FILE) as conn:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE crude
        CREATE TABLE organized
    """)
