#!/usr/bin/env python3

"""
runs everytime a new user is created
TODO: create a ``unSetup.py``
"""

import sqlite3

STAGING_FILE = "staging.db"

with sqlite3.connect(STAGING_FILE) as conn:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE
    """)
