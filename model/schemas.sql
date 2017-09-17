`
link has-many intel

link has-many tags
tag has-many links

link has-many projects
project has-many links

computer(sys+locn) has-many links
`


CREATE TABLE links
( linkID 
, 
)
/*
crude is a subset of organized IF we ignore SESSION_INDICATOR
*/

linkID, url, state(orgz, un-orgz, err), title, is_porn, _timestamp

TAGS
	tagID, tag_name
	TAG_CONGLO
		id, iFK_linkID, iFK_tagID

PROJECTS
	projectID, project_name
	PROJECT_CONGLO
		id, iFK_linkID, iFK_projectID

INTELLIGENCE
	id, linkID, _timestamp, info






