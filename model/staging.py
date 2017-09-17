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
from bs4 import BeautifulSoup
from collections import namedtuple
from contextlib import contextmanager

import utils



# constants and data structs--------------------------------------------------

Clean = namedtuple("Clean",
	[ "url"
	, "title"
	, "safeForWork"
	, "date_created"
	, "state_"
	, "import_"])



# functions-------------------------------------------------------------------

@contextmanager
def sqliteDB(file_name):
	conn = sqlite3.connect(file_name)
	yield conn.cursor()
	conn.commit()
	conn.close()
	return

def process(crude_data, importID, oldData):
	state_ = "staging"
	import_ = importID

	url = crude_data.url
	top = utils.partialDownload(1024)	# TODO: this needs to be incremental if title finding fails
	# TODO: this needs to be async
	title = BeautifulSoup(top).find_all("title")[0].get_text()
	safeForWork = "NotImplemented"
	date_created = crude_data.raw_add_date

	info4intel = crude_data.context
	if len(crude_data.raw_title) <= len(title):
		# entire thing is a comment or a true-copy
		if title == crude_data.raw_title:	pass	# no intel
		else:
			info4intel.append(crude_data.raw_title)
	else:
		# (original) title is short => comment is perhaps prepended
		a, _, b = crude_data.raw_title.partition(title)
		worthy = list(filter(None, [a, b]))
		info4intel += worthy
	if oldData:
		if date_created == oldData.date_created \
		and 
		if title != oldData.title:	# rare but possible
			title = oldData.title

	clean_data = Clean._make(
		[url, title, safeForWork, date_created, state_, import_]
	)
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
			"SELECT _id FROM computer WHERE system=? AND location=?",
			[system, location])
			reticle = x.fetchone()[0]
		else:
			reticle = cur.lastrowid

	with open(file_path, mode='rt') as fh:
		plain_text = fh.read()
	hashVal = utils.calc_hash(file_path)
	timestamp = int(time.time())
	with sqliteDB(dbFile) as cur:
		try:
			cur.execute(
			"INSERT INTO imports (ts_on_zAxis, hash, file_contents, computer_id) VALUES (?,?,?,?)",
			[timestamp, hashVal, plain_text, reticle])
		except:
			x = cur.execute("SELECT ts_on_zAxis, computer_id FROM imports WHERE hash=?", [hashVal])
			x = x.fetchall()[0]
			raise RuntimeError("File already imported on {0} from {1}".format(x[0], x[1]))
			return
		else:
			importID = cur.lastrowid

	for aCrude in raw_data:
		? if url exists in db get it as obj () and old_importID (ts_on_zAxis, computer & location)
		semi = process(aCrude, importID, oldData)
		INSERT...
	return
