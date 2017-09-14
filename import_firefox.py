#!/usr/bin/env python3

# TODO: try lxml
from bs4 import BeautifulSoup

context = list()
debutant = str()	# empty string, representing the very first debutant i.e.
					# the namesless folder/category where all bookmarks go by
					# default

def process(line):
	soup = BeautifulSoup(line)
	if soup.find_all("a"):
		# this line is a link container
		_obj = soup.find_all("a")[0]
		url = _obj.get('href')
		title = _obj.get_text()
		timestamp = _obj.get('add_date')
		return (url, title, timestamp, context)
	elif soup.find_all('h3'):
		# this line contains category/folder related info
		debut_ready = soup.find_all("h3")[0].get_text()
		global debutant
		debutant = debut_ready
		# we are not appending ``debut_ready`` to ``context`` just yet because
		# <DL> appears first, at 0 indent, before any <H3> and hence, we wait
		# until a DL is found JUST after H3
		return None
	elif soup.find_all('dl'):
		# nesting begin hint
		global context
		context.append(debutant)
		return None
	elif "</dl" in line.lower():
		# de-nesting begin hint
		context.pop()
		return None
	else:
		# this line is not intersting
		return False
	return

def main(file_path):
	with open(file_path, mode='rt') as fh:
		for aLine in fh:
			ans = process(aLine)
			if ans:
				# add to ``unorganized`` db
				print(ans[1])
	assert len(context) == 0	# since last DL has been closed
	return

if __name__ == '__main__':
	main('./samples/firefox.html')
