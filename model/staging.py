#!/usr/bin/env python3

"""
when import_bookmark.py runs, it returns a list of tuples, the contents of
which are as follows
	url
	title
	timestamp
	context (which helps in suggesting tags)
the purpose of this file is to
	store above schema in a database
	aid transition of data in immature phase to ripe phase
"""

import sqlite3
from collections import namedtuple
from contextlib import contextmanager

Crude = namedtuple("Crude",		# no need to use class in this case because
	[ "url"						# the data is being dumped to SQLite DB not
	, "title"					# JSON so custom encoder/decoder need not be
	, "timestamp"				# defined and ``namedtuple`` will suffice
	, "context" ])

@contextmanager
def sqliteDB(file_name):
	conn = sqlite3.connect(file_name)
	cur = conn.cursor()
	yield cur
	conn.commit()
	conn.close()
	return
