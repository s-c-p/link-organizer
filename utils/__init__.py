#!/usr/bin/env python3

import hashlib
import datetime

ONE_MB = 1048576

humanizeTime = lambda unixEpoch = datetime.datetime.fromtimestamp(unixEpoch)

def calc_hash(file_path):
	hasher = hashlib.sha256()
	with open(file_path, mode="rb") as fh:
		for aBlock in iter(lambda: fh.read(ONE_MB), b""):
			hasher.update(aBlock)
	return hasher.hexdigest()

