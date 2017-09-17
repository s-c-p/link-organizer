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

def humanizeUA(uaString):
	# TODO
	return uaString

def partialDownload(url, max_bytes):
	# NOTE: stackoverflow.com/q/23602412/
	# maybe use github.com/alecxe/scrapy-fake-useragent
	try:
		import requests
	except ImportError:
		import socket, time
		tcp_port = 80
		MAX_LIMIT = max_bytes
		from urllib.parse import urlsplit
		x = urlsplit(url)
		tcp_host = x.netloc
		i = url.index(tcp_host)+len(tcp_host)
		remaining = url[i:]
		del x, i, urlsplit
		message = \
		"GET {0} HTTP/1.1\r\n" \
		"HOST: {1}\r\n" \
		"User-Agent: Custom/0.0.1\r\n" \
		"Accept: */*\r\n\n".format(remaining, tcp_host)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
		s.connect((tcp_host, tcp_port)) # Connect to remote socket at given address
		s.send(message) # Let's begin the transaction
		time.sleep(0.1)
		# Keep reading from socket till max limit is reached
		data = ""
		curr_size = int()
		while curr_size < MAX_LIMIT:
			data += s.recv(MAX_LIMIT - curr_size)
			curr_size = len(data)
		s.close()
	else:
		headers = {"Range": "bytes=0-"+str(max_bytes)}
		r = requests.get(url, headers=headers)
		data = r.content
	return data
