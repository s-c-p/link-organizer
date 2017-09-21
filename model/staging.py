#!/usr/bin/env python3

"""
when bulk_import.py runs, it returns a list of tuples, the contents of
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

def process(crude_data, importID):
	state_ = "staging"
	import_ = importID
	url = crude_data.url
	top = utils.partialDownload(1024)	# TODO: this needs to be incremental if title finding fails
	# TODO: this needs to be async
	title = BeautifulSoup(top).find_all("title")[0].get_text()
	safeForWork = NotImplemented
	date_created = crude_data.raw_add_date
	return Clean._make(
		[url, title, safeForWork, date_created, state_, import_]
	)

def basicIntel(clean_data, old_title, context):
	info4intel = context
	if len(old_title) <= len(title):
		# entire thing is a comment or a true-copy
		if clean_data.title == old_title:	pass	# no intel
		else:
			info4intel.append(old_title)
	else:
		# (original) title is short => comment is perhaps prepended
		a, _, b = old_title.partition(title)
		worthy = list(filter(None, [a, b]))
		info4intel += worthy
	return info4intel

def advancedIntel(oldData, newData):
	# if importID matches, then this should have never happened in the
	# first place because of the error raised by initNewImport
	""" derive intel, check reps
	now now, link can repeat in an entirely different import or in incremental import
		SO if link && computer && adddate match, ignore
		if adddate or computer is different increase count in intel
		if comment is different inform intel
	title
	safeForWork
	date_created
	state_id
	import_id
	"""
	if newData.date_created == oldData.date_created \
	and 
	if title != oldData.title:	# rare but possible
		title = oldData.title
	return

def initNewImport(file_path):
	hashVal = utils.calc_hash(file_path)
	timestamp = int(time.time())
	with open(file_path, mode='rt') as fh:
		plain_text = fh.read()
	with sqliteDB(dbFile) as cur:
		try:
			cur.execute(
			"INSERT INTO imports (file_contents, ts_on_zAxis, hash) VALUES (?,?,?)",
			[plain_text, timestamp, hashVal])
		except sqlite3.IntegrityError:
			# UNIQUE constraint failed: imports.hash
			x = cur.execute("SELECT ts_on_zAxis, computer_id FROM imports WHERE hash=?", [hashVal])
			x = x.fetchall()[0]
			raise RuntimeError("File already imported on {0} from {1}".format(x[0], x[1])) from None
		else:
			importID = cur.lastrowid
	return importID

def insertCleanData(clean_data):
	url = clean_data.url
	title = clean_data.title
	state_id = utlty_deENUMfunc(clean_data.state_)
	import_id = clean_data.import_
	safeForWork = clean_data.safeForWork
	date_created = clean_data.date_created
	# search `sqlite3 namedtuple` and look at 
	# http://peter-hoffmann.com/2010/python-sqlite-namedtuple-factory.html
	with sqliteDB(dbFile) as cur:
		cur.execute(
		"INSERT INTO links (url, title, safeForWork, date_created, state_id, import_id) VALUES (?,?,?,?,?,?)"
		[url, title, safeForWork, date_created, state_id, import_id])
		linkID = cur.lastrowid
	return linkID

def stage(file_path, raw_data):
	importID = initNewImport(file_path)
	for aCrude in raw_data:
		# ? if url exists in db get it as obj () and old_importID (ts_on_zAxis, computer & location)
		# semi = process(aCrude, importID, oldData)
		# INSERT...
		context = aCrude.context
		old_title = aCrude.raw_title
		clean_data = process(aCrude, importID)
		base_intel = basicIntel(clean_data, old_title, context)
		try:
			linkID = insertCleanData(clean_data)
		except sqlite3.IntegrityError:
			# => url already exists, time to increase intel
			newData = clean_data
			oldData = utlty_getOldLink(newData.url)
			diff_based_intel = advancedIntel(oldData, newData)
			# NOTE: newData.import_ == oldData.import_ will never happen under normal flow of control
			update_db(newData)
		finally:
			insert base_intel & diff_based_intel if it exists INTO `link`
	return

def utlty_getOldLink(url):
	with sqliteDB(dbFile) as cur:
		x = cur.execute(
		"SELECT url, title, safeForWork, date_created, state_id, import_id FROM links WHERE url=?",
		[url])
		x = x.fetchone()
	ans = Clean(*x)
	return ans

def utlty_deENUMfunc(state):
	ans = 2
	# NOTE: why hardcoded? because we can read from DB but the
	# value is gonna be constant so hardcoded
	return ans
