#!/usr/bin/env python3

"""
	Works nicely on:
		chrome
		firefox
		opera
	Not tested on:
		safari		TODO

	TODO: try lxml, because is lean and faster, but do take a look at:
		- stackoverflow.com/q/16322862/
		- stackoverflow.com/q/2723015/
		- lxml.de/lxmlhtml.html
		- bit.ly/2fr3Vo9
"""

import re
from bs4 import BeautifulSoup
from collections import namedtuple




URL_REGEX = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

Raw = namedtuple("Raw",
	[ "url"
	, "raw_title"
	, "raw_add_date"
	, "intel"])




context = list()
debutant = str()	# empty string, representing the very first debutant i.e.
					# the namesless folder/category where all bookmarks go by
					# default




def process(line):
	""" experince revealed that this func works perfectly with:
		<!DOCTYPE NETSCAPE-BOOKMARK-FILE-1>
	TODO: information is almost never useless, in further iterations try to
	preserve misc information like comments, DD, etc.
	TODO: turns out <!DOCTYPE NETS...> also handles stuff like feeds &
	webslices, read bit.ly/2fcIPx3 to make this function more robust
	"""
	soup = BeautifulSoup(line, 'lxml')
	if soup.find_all("a"):
		# this line is a link container
		_obj = soup.find_all("a")[0]
		url = _obj.get('href')
		title = _obj.get_text()
		timestamp = _obj.get('add_date')
		local_context = list(filter(None, context))
		return Raw._make([url, title, timestamp, local_context])
	elif soup.find_all('h3'):
		# this line contains category/folder related info
		debut_ready = soup.find_all("h3")[0].get_text()
		globals()["debutant"] = debut_ready
		# we are not appending ``debut_ready`` to ``context`` just yet because
		# <DL> appears first, at 0 indent, before any <H3> and hence, we wait
		# until a DL is found JUST after H3
		return None
	elif soup.find_all('dl'):
		# HINT: nesting begin
		globals()["context"].append(debutant)
		return None
	elif "</dl" in line.lower():
	# elif line.strip().lower().startswith("</dl"):
		# HINT: de-nesting begin
		globals()["context"].pop()
		return None
	else:
		# this line is not intersting
		return False
	return

def standard_importer(file_path):
	raw_data = list()
	with open(file_path, mode='rt') as fh:
		for aLine in fh:
			ans = process(aLine)
			if ans:
				raw_data.append(ans)
				print(ans.intel)
	assert len(context) == 0	# since last DL has been closed
	return raw_data

def non_standard_importer(file_path):
	""" my habit is to use tab-indentation to put a list of links under
	a topic, others may do it differently
	AND for this reason, it is really important that we keep a copy of
	the original import-file in database
	"""
	regex = re.compile(URL_REGEX)
	timestamp = int(os.stat(file_path).st_mtime)
	with open(file_path, mode="rt") as fh:
		for aLine in fh:
			links = regex.findall(aLine)
			for link in links:
				ans = Raw._make([link, aLine, timestamp, []])
				raw_data.append(ans)
	return raw_data

if __name__ == '__main__':
	standard_importer('./test-data/bookmark-samples/opera.html')
	standard_importer('./test-data/bookmark-samples/chrome.html')
	standard_importer('./test-data/bookmark-samples/firefox.html')
	# non_standard_importer('./test-data/bookmark-samples/samp.txt')
