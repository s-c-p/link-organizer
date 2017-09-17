#!/usr/bin/env python3

"""
when import_bookmark.py runs, it returns a list of tuples, the contents of
which are as follows
	url
	title
	timestamp
	context (which helps in suggesting tags)
and an additional field which would indicate the date/session when a given set
of bookmarks were imported to the staging area (this is important from UX POV
and will not be forwarded to organized.db)
	SESSION_INDICATOR
note that SESSION_INDICATOR will be same for all links imported at once so its
a one-to-many relationship

the purpose of this file is to
	store above schema in a database
	aid transition of data in immature phase to ripe phase
"""

import base64
import hashlib
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
	yield conn.cursor()
	conn.commit()
	conn.close()
	return

def calc_hash(file_path):
	hasher = hashlib.sha256()
	with open(file_path, mode="rb") as fh:
		for aBlock in iter(lambda: fh.read(1048576), b""):
			hasher.update(aBlock)
	return hasher.hexdigest()

def stage(raw_data, file_path):
	""" derive intel, check reps
	now now, link can repeat in an entirely different import or in incremental import
		SO if link && computer && adddate match, ignore
		if adddate or computer is different increase count in intel
		if comment is different inform intel

	"""
	return

