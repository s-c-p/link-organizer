`
Files affected by changes in this file:
	setup.py, staging.py
`

/*
crude is a subset of organized IF we ignore SESSION_INDICATOR
*/
`
I think 'computer' table is really useless, but anyway
one computer can make many imports
and the same file may be imported from 1+ computers
`

CREATE TABLE computers
( computerID INTEGER PRIMARY KEY AUTOINCREMENT
, system TEXT NOT NULL
, location TEXT
, CONSTRAINT succintness UNIQUE (system, location)
);

CREATE TABLE imports
( importID INTEGER PRIMARY KEY AUTOINCREMENT
, file_contents TEXT
, ts_on_zAxis TIMESTAMP
, hash TEXT(40) NOT NULL
, CONSTRAINT succintness UNIQUE (hash)
);

CREATE TABLE incoming_files
( _id INTEGER PRIMARY KEY AUTOINCREMENT
, FK_importID INTEGER NOT NULL
, FK_computerID INTEGER NOT NULL
, FOREIGN KEY (FK_importID) REFERENCES imports(importID)
, FOREIGN KEY (FK_computerID) REFERENCES computers(computerID)
, CONSTRAINT xyz UNIQUE (FK_importID, FK_computerID)
);




`
link has 3 states, i.e. state has-many links
link has-many informations (which togather provide intel)
`
CREATE TABLE enum_states
( _id INTEGER PRIMARY KEY AUTOINCREMENT
, state TEXT NOT NULL
); INSERT INTO enum_states (state) VALUES
("tagged"), ("staging"), ("err");

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
, CONSTRAINT succintness UNIQUE (url)
);

CREATE TABLE intel
( intelID INTEGER PRIMARY KEY AUTOINCREMENT
, FK_linkID INTEGER
, information TEXT NOT NULL
, ts_on_zAxis TIMESTAMP
, FOREIGN KEY (FK_linkID) REFERENCES links(linkID)
);




`
link   has-many   tags   AND
tag    has-many   links  ALL
connections are stored in categories
`
CREATE TABLE tags
( tagID INTEGER PRIMARY KEY AUTOINCREMENT
, tag_name TEXT NOT NULL
);
CREATE TABLE categories
( _id INTEGER PRIMARY KEY AUTOINCREMENT
, FK_tagID INTEGER
, FK_linkID INTEGER
, FOREIGN KEY (FK_tagID) REFERENCES tags(tagID)
, FOREIGN KEY (FK_linkID) REFERENCES links(linkID)
, CONSTRAINT succintness UNIQUE (FK_tagID, FK_linkID)
);




`
link      has-many   projects  AND
project   has-many   links     ALL
connections are stored in project_tracker
`
CREATE TABLE projects
( projectID INTEGER PRIMARY KEY AUTOINCREMENT
, project_name TEXT NOT NULL
);
CREATE TABLE project_tracker
( _id INTEGER PRIMARY KEY AUTOINCREMENT
, FK_linkID INTEGER
, FK_projectID INTEGER
, FOREIGN KEY (FK_linkID) REFERENCES links(linkID)
, FOREIGN KEY (FK_projectID) REFERENCES projects(projectID)
, CONSTRAINT succintness UNIQUE (FK_projectID, FK_linkID)
);
