#!/usr/bin/env python3

"""
	Works nicely on:
		chrome
		firefox
	Works satisfactorily on:
		opera
	Not tested on:
		safari		TODO

	TODO: information is almost never useless, in further iterations try to
	preserve misc information like comments, DD, etc.

	TODO: try lxml, but take a look at
		stackoverflow.com/q/16322862/
		stackoverflow.com/q/2723015/
		lxml.de/lxmlhtml.html
		bit.ly/2fr3Vo9
"""

from bs4 import BeautifulSoup
from collections import namedtuple

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

def main(file_path):
	raw_data = list()
	with open(file_path, mode='rt') as fh:
		for aLine in fh:
			ans = process(aLine)
			if ans:
				# raw_data.append(ans)
				print(ans.intel)
	assert len(context) == 0	# since last DL has been closed
	return

if __name__ == '__main__':
	main('./test-data/bookmark-samples/opera.html')
	main('./test-data/bookmark-samples/chrome.html')
	main('./test-data/bookmark-samples/firefox.html')
