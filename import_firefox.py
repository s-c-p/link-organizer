#!/usr/bin/env python3

from bs4 import BeautifulSoup
# TODO: try lxml

context = list()

def what_does_line_tell(line):
	soup = BeautifulSoup(line)
	if soup.find_all('a'):
		return "link container"
	elif soup.find_all('h3'):
		return "title/category/folder container"
	elif soup.find_all('dl') or "</dl" in line.lower():
		return "nesting hint"
	else:
		return False

interesting = what_does_line_tell

def process(line):
	if not interesting(line):
		return False
	type_of_line = what_does_line_tell(line)
	if type_of_line == "link container":
		obj = BeautifulSoup(line).find_all("a")[0]
		url = obj.get('href')
		title = obj.get_text()
		timestamp = obj.get('add_date')
		return (url, title, timestamp)
	elif type_of_line == "title/category/folder container":
		debut_ready = BeautifulSoup(line).find_all("h3")[0].get_text()
		global debutant
		debutant = debut_ready
		return None
	elif type_of_line == "nesting hint":
		global context
		if "<dl>" in line.lower():
			context.append(debut_ready)
			# pass	# because before this line, the previousLine's processing would have invoked creation of debutant
		else:
			context.pop()
		return None
	return

def main(file_path):
	with open(file_path, mode='rt') as fh:
		previousLine = str()
		for aLine in fh:
			process(aLine)
	assert len(context) == 0	# since last DL has been closed
	return
