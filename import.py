with open(file_name) as fp:
    head = fp.readline()

if head.lower().startswith("<!doctype netscape-bookmark-file-1>"):
    import import_bookmarks as ib
    importer = ib.main
else:
    