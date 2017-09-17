#!/usr/bin/env python3

"""
runs everytime a new user is created
TODO: create a ``unSetup.py``
"""

import os
import sqlite3

USER_FILE = "1655df96-89f1-494c-955a-25758a93e104"

def initializeDB(USER_FILE):
	conn = sqlite3.connect(USER_FILE)
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE computer
		( _id INTEGER PRIMARY KEY AUTOINCREMENT
		, system TEXT NOT NULL
		, location TEXT NOT NULL
		);
	""")
	cur.execute("""
		CREATE TABLE imports
		( importID INTEGER PRIMARY KEY AUTOINCREMENT
		, hash TEXT(40) NOT NULL
		, b85_file TEXT
		, computer_id INTEGER
		, FOREIGN KEY (computer_id) REFERENCES computer(_id)
		);
	""")
	cur.execute("""
		CREATE TABLE enum_states
		( _id INTEGER PRIMARY KEY AUTOINCREMENT
		, state TEXT NOT NULL
		);
	""")
	cur.execute("""
		INSERT INTO enum_states (state) VALUES
		("tagged"), ("staging"), ("err");
	""")
	cur.execute("""
		CREATE TABLE links
		( linkID INTEGER PRIMARY KEY AUTOINCREMENT
		, url TEXT NOT NULL
		, title TEXT NOT NULL
		, safeForWork BOOLEAN
		, date_created TIMESTAMP
		, state_id INTEGER
		, import_id INTEGER
		, FOREIGN KEY (state_id) REFERENCES enum_states(_id)
		, FOREIGN KEY (import_id) REFERENCES import(importID)
		);
	""")
	cur.execute("""
		CREATE TABLE intel
		( intelID INTEGER PRIMARY KEY AUTOINCREMENT
		, FK_linkID INTEGER
		, information TEXT NOT NULL
		, ts_on_zAxis TIMESTAMP
		, FOREIGN KEY (FK_linkID) REFERENCES links(linkID)
		);
	""")
	cur.execute("""
		CREATE TABLE tags
		( tagID INTEGER PRIMARY KEY AUTOINCREMENT
		, tag_name TEXT NOT NULL
		);
	""")
	cur.execute("""
		CREATE TABLE categories
		( _id INTEGER PRIMARY KEY AUTOINCREMENT
		, FK_tagID INTEGER
		, FK_linkID INTEGER
		, FOREIGN KEY (FK_tagID) REFERENCES tags(tagID)
		, FOREIGN KEY (FK_linkID) REFERENCES links(linkID)
		, CONSTRAINT succintness UNIQUE (FK_tagID, FK_linkID)
		);
	""")
	cur.execute("""
		CREATE TABLE projects
		( projectID INTEGER PRIMARY KEY AUTOINCREMENT
		, project_name TEXT NOT NULL
		);
	""")
	cur.execute("""
		CREATE TABLE project_tracker
		( _id INTEGER PRIMARY KEY AUTOINCREMENT
		, FK_linkID INTEGER
		, FK_projectID INTEGER
		, FOREIGN KEY (FK_linkID) REFERENCES links(linkID)
		, FOREIGN KEY (FK_projectID) REFERENCES projects(projectID)
		, CONSTRAINT succintness UNIQUE (FK_projectID, FK_linkID)
		);
	""")
	conn.commit()
	conn.close()
	return

if __name__ == '__main__':
	initializeDB(USER_FILE)
	# os.remove(USER_FILE)