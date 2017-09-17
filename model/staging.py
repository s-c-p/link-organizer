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

import time
import sqlite3
from collections import namedtuple
from contextlib import contextmanager

import utils




Crude = namedtuple("Crude",		# no need to use class in this case because
	[ "url"						# the data is being dumped to SQLite DB not
	, "title"					# JSON so custom encoder/decoder need not be
	, "timestamp"				# defined and ``namedtuple`` will suffice
	, "context" ])
Clean = namedtuple("Clean",
	[ ""])



@contextmanager
def sqliteDB(file_name):
	conn = sqlite3.connect(file_name)
	yield conn.cursor()
	conn.commit()
	conn.close()
	return

def proc(raw_data):
	utils.partialDownload
	return clean_data

def stage(file_path, raw_data, uaString, location):
	""" derive intel, check reps
	now now, link can repeat in an entirely different import or in incremental import
		SO if link && computer && adddate match, ignore
		if adddate or computer is different increase count in intel
		if comment is different inform intel

	"""
	system = utils.humanizeUA(uaString)
	with sqliteDB(dbFile) as cur:
		try:
			cur.execute(
			"INSERT INTO computer (system, location) VALUES (?,?)",
			[system, location])
		except sqlite3.IntegrityError:
			x = cur.execute(
			"SELECT_id FROM computer WHERE system=? AND location=?",
			[system, location])
			reticle = x.fetchone()[0]
		else:
			reticle = cur.lastrowid
	with open(file_path, mode='rt') as fh:
		plain_text = fh.read()
	hashVal = utils.calc_hash(file_path)
	timestamp = int(time.time())
	with sqliteDB(dbFile) as cur:
		cur.execute(
		"INSERT INTO imports (ts_on_zAxis, hash, file_contents, computer_id) VALUES (?,?,?,?)",
		[timestamp, hashVal, plain_text, reticle])
	clean_data = process(raw_data)
	return


