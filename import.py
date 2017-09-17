#!/usr/bin/env python3

import utils.bulk_importer as bi
from model.staging import stage

def main(file_name):
	with open(file_name) as fp:
		head = fp.readline()
	if head.lower().startswith("<!doctype netscape-bookmark-file-1>"):
		importer = bi.standard_importer
	else:
		importer = bi.non_standard_importer
	raw_data = importer(file_name)
	stage(raw_data, file_name)
	return

if __name__ == '__main__':
	main()
