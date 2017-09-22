#!/usr/bin/env python3

"""
when bulk_import.py runs, it returns a list of Raw/Crude objects, the contents
of which are
	url (may be partial)
	title (as stored by user and not of the webpage itself)
	timestamp (as reported by browser)
	context (which helps in suggesting tags)

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

def initNewImport(file_path):
	hashVal = utils.calc_hash(file_path)
	timestamp = int(time.time())
	with open(file_path, mode='rt') as fh:
		plain_text = fh.read()
	with sqliteDB(dbFile) as cur:
		try:
			cur.execute(
				"INSERT INTO imports " 					\
				"(file_contents, ts_on_zAxis, hash) "	\
				"VALUES (?,?,?)", [plain_text, timestamp, hashVal]
			)
		except sqlite3.IntegrityError:
			# UNIQUE constraint failed: imports.hash
			x = cur.execute(
				"SELECT ts_on_zAxis FROM imports WHERE hash=?",
				[hashVal]
			)
			x = x.fetchall()[0]
			raise RuntimeError("File already imported on {0}".format(x[0]))
		else:
			importID = cur.lastrowid
	return importID

def process(crude_data, importID):
	state_ = "staging"
	import_ = importID
	url = crude_data.url
	# TODO: the following needs to be incremental if title finding fails
	top = utils.partialDownload(1024)
	# TODO: this needs to be async
	title = BeautifulSoup(top).find_all("title")[0].get_text()
	safeForWork = NotImplemented
	date_created = crude_data.raw_add_date
	return Clean._make(
		[url, title, safeForWork, date_created, state_, import_]
	)

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
			"INSERT INTO links "											\
			"(url, title, safeForWork, date_created, state_id, import_id) "	\
			"VALUES (?,?,?,?,?,?)",
			[url, title, safeForWork, date_created, state_id, import_id]
		)
		linkID = cur.lastrowid
	return linkID

?def basicIntel(clean_data, old_title, context):
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
	""" returns difference based intelligence if any
	url
		IS IDENTICAL, thats why we are here
	title
		no intel is found in the title in this scenario because whatever intel
		was available was already processed by basicIntel and these titles
		are extracted from the downloaded webpage
		**new change worth recording (cuz this is the ORIGINAL title that
		web-author gave, any comments associated would've been added to
		link's intel already)
	safeForWork
		new change worth recording (with prompt)
		cuz machine learing api will only get smarter by the day
	date_created
		doesn't tell anything alone, look at import_id
	state_id
		doesn't matter; if both are , new is `staging` old is `organized`
	import_id
		HAS TO BE DIFFERENT, => 
	"""
	final = newData
	info4intel = list()
	# if importID matches, then this should have never happened in the
	# first place because of the error raised by initNewImport
	assert oldData.import_ != newData.import_
	if newData.date_created == oldData.date_created:
		# this is a case of incremental import
		pass
	else:
		a = oldData.date_created
		b = newData.date_created
		final.date_created = min(a, b)
		info4intel.append(f"date_created {a}")
		info4intel.append(f"date_created {b}")
	if newData.title != oldData.title:	# rare but possible
		final.title = newData.title
		info4intel.append(oldData.title)
	if newData.safeForWork != oldData.safeForWork:
		final.safeForWork = newData.safeForWork
	# TODO
	# if newData.state_ != oldData.state_:
	return final, info4intel

def updateLinkDetails(linkID, clean_data):
	with sqliteDB(dbFile) as cur:
		cur.execute(
			"UPDATE links " 		\
			"SET " 					\
			"	url=?, " 			\
			"	title=?, " 			\
			"	safeForWork=?, " 	\
			"	date_created=?, " 	\
			"	state_id=?, " 		\
			"	import_id=? " 		\
			"WHERE " 				\
			"	linkID=?;"
			[url, title, safeForWork, date_created, state_id, import_id, \
			linkID]
		)
		linkID = cur.lastrowid
	return

def insertIntel(linkID, timestamp, infoSet):
	with sqliteDB(dbFile) as cur:
		for piece in infoSet:
			cur.execute(
				"INSERT INTO intel "\
				"(FK_linkID, information, ts_on_zAxis) "\
				"VALUES (?,?,?)", [linkID, str(piece), timestamp]
			)
	return

def stage(file_path, raw_data):
	importID = initNewImport(file_path)
	for aCrude in raw_data:
		# ? if url exists in db get it as obj () and old_importID (ts_on_zAxis,
		# computer & location)
		# semi = process(aCrude, importID, oldData)
		# INSERT...
		context = aCrude.context
		old_title = aCrude.raw_title
		timestamp = int(time.time())	# needed for inserting intel data
		clean_data = process(aCrude, importID)
		base_intel = basicIntel(clean_data, old_title, context)
		try:
			linkID = insertCleanData(clean_data)
		except sqlite3.IntegrityError:
			# => url already exists, time to increase intel
			newData = clean_data
			linkID, oldData = utlty_getOldLink(newData.url)
			final, diff_intel = advancedIntel(oldData, newData)
			# NOTE: newData.import_ == oldData.import_ will never happen under
			# normal flow of control
			if final == oldData:
				pass
			else:
				updateLinkDetails(linkID, final)
				insertIntel(linkID, timestamp, diff_intel)
		insertIntel(linkID, timestamp, base_intel)
	return

def utlty_getOldLink(url):
	with sqliteDB(dbFile) as cur:
		x = cur.execute(
			"SELECT "							\
			"linkID, url, title, safeForWork, "	\
			"date_created, state_id, import_id "\
			"FROM links WHERE url=?", [url]
		)
		x = x.fetchone()
	ans = Clean(x[1:])
	linkID = x[0]
	assert type(ans.import_id) is int
	return ans

def utlty_deENUMfunc(state):
	ans = 2
	# NOTE: why hardcoded? because we can read from DB but the
	# value is gonna be constant so hardcoded
	return ans
