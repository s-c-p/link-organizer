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

class Link(object):
	""" although Link data struct needs nothing more than to be a C struct,
	but I left the simplicity of collections.namedtuple to provide API for 
	database operations C(save)R(getDetailsByURL)U(update)D(not-applicable)
	And thats it, I have not defined any other methods because i wanna stick
	to functional programming and avoid OOP as much as possible, which is
	further illustrated by ``stackoverflow.com/q/390250/``, reason why I did
	not define an internal equality calculator
	"""
	def __init__(self, url, title, safeForWork, date_created,
		state_, import_):
		self.url = url
		self.title = title
		self.safeForWork = safeForWork
		self.date_created = date_created
		self.state_ = state_
		self.import_ = import_
		return

	def save(self):
		""" save itself in the database and return the reference key """
		# search `sqlite3 namedtuple` and look at 
		# http://peter-hoffmann.com/2010/python-sqlite-namedtuple-factory.html
		with sqliteDB(dbFile) as cur:
			cur.execute(
				"INSERT INTO links "						\
				"(url, title, safeForWork, date_created, "	\
				"state_id, import_id) "						\
				"VALUES (?,?,?,?,?,?)",
				[self.url, self.title, self.safeForWork, self.date_created,
				utlty_deENUMfunc(self.state_), self.import_]
			)
			linkID = cur.lastrowid
		return linkID

	@staticmethod
	def getDetailsByURL(self, url):
		""" fetch all information from DB of a link based solely on any
		arbitrary url and not bound by the instance/object on which it is
		called and hence this is a ``staticmethod``
		"""
		with sqliteDB(dbFile) as cur:
			x = cur.execute(
				"SELECT "							\
				"linkID, url, title, safeForWork, "	\
				"date_created, state_id, import_id "\
				"FROM links WHERE url=?", [url]
			)
			x = x.fetchone()
		linkID = x[0]
		params = x[1:]
		ans = Link(*params)
		assert type(ans.import_id) is int
		return linkID, ans

	@staticmethod
	def update(self, targetID, idol):
		""" update...
		the only reason I am taking targetID as a parameter is because it is
		already available where its gonna be needed, provided by other
		functions and we can avoid a new database read operation, IDEALLY
		though it should be Link.update(old, new) --> and the func derives
		targetID from ``old``
		"""
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
				[idol.url, idol.title, idol.safeForWork,
				idol.date_created, idol.state_id, idol.import_id,
				targetID]
			)
		return


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
				"SELECT ts_on_zAxis FROM imports WHERE hash=?", [hashVal]
			)
			x = x.fetchall()[0]
			timestamp = x[0]
			humanTime = utils.humanizeTime(timestamp)
			raise RuntimeError(f"File already imported on " \
				"{timestamp}, i.e. {humanTime}"
			)
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
	return Link(
		url, title, safeForWork, date_created, state_, import_
	)

def basicIntel(clean_data, bkmk_title, context):
	info4intel = context
	if len(bkmk_title) <= len(title):
		# entire thing is a comment or a true-copy
		if clean_data.title == bkmk_title:	pass	# no intel
		else:
			info4intel.append(bkmk_title)
	else:
		# (original) title is short => comment is perhaps prepended
		a, _, b = bkmk_title.partition(title)
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
	# rare but possible
	if newData.title != oldData.title:
		final.title = newData.title
		info4intel.append(oldData.title)
	if newData.safeForWork != oldData.safeForWork:
		final.safeForWork = newData.safeForWork
	# TODO
	# if newData.state_ != oldData.state_:
	return final, info4intel

def utlty_deENUMfunc(state):
	ans = 2
	# NOTE: why hardcoded? because we can read from DB but the
	# value is gonna be constant so hardcoded
	return ans

def areLinksEqual(linkA, linkB):
	try:
		assert isinstance(linkA, Link)
	except AssertionError:
		return False
	else:
		# why not using linkA.__dict__ == linkB.__dict__?
		# see ``stackoverflow.com/q/390250/``
		ans = \
		linkA.url == linkB.url and \
		linkA.title == linkB.title and \
		linkA.state_ == linkB.state_ and \
		linkA.import_ == linkB.import_ and \
		linkA.safeForWork == linkB.safeForWork and \
		linkA.date_created == linkB.date_created
	return ans

def insertIntel(linkID, timestamp, infoSet):
	with sqliteDB(dbFile) as cur:
		for piece in infoSet:
			cur.execute(
				"INSERT INTO intel "					\
				"(FK_linkID, information, ts_on_zAxis) "\
				"VALUES (?,?,?)",
				[linkID, str(piece), timestamp]
			)
	return

def stage(file_path, raw_data):
	importID = initNewImport(file_path)
	for aCrude in raw_data:
		# needed for inserting intel data
		timestamp = int(time.time())
		context = aCrude.context
		bkmk_title = aCrude.raw_title
		clean_data = process(aCrude, importID)
		# not yet sure wheather we're gonna need it (or not) but still we
		# derive it for the sake of DRY
		base_intel = basicIntel(clean_data, bkmk_title, context)
		try:
			linkID = clean_data.save()
		except sqlite3.IntegrityError:
			# => url already exists, time to increase intel
			newData = clean_data
			linkID, oldData = Link.getDetailsByURL(newData.url)
			final, diff_intel = advancedIntel(oldData, newData)
			# NOTE: newData.import_ == oldData.import_ will never happen under
			# normal flow of control
			if areLinksEqual(final, oldData):
				# this is the case of incremental import_
				# no updation of link's attributes and no new intel if found
				pass
			else:
				# same link was stored on 2 different systems/locations and
				# probably has different comments/tags/etc. which can give
				# helpful information
				Link.update(linkID, final)
				insertIntel(linkID, timestamp, base_intel)
				insertIntel(linkID, timestamp, diff_intel)
		else:
			# Link is definately new & hence intel is new
			insertIntel(linkID, timestamp, base_intel)
	return
