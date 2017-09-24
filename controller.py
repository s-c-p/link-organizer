import bottle

@bottle.route("/")
def index():
	# organized_count
	# pending_count
	# errors_count
	# **** tag_cloud
	# **** project_cloud
	return bottle.template("view/index")

# search----------------------------------------------------------------------

@bottle.route("/search")
def search():
	return

# view links------------------------------------------------------------------

@bottle.route("/view_links")
def view_links():
	# isThisFirstPage
	# pageNum
	# table_body
	curate(fetched_links, config) # NOTE: link is inactive if vpn-required==true, and to wikipedia's-porn page if sfw==false
	return bottle.template("view/view_links")

# organize links--------------------------------------------------------------

@bottle.route("/organize_links")
def organize_links():
	if sessionID not in GET_request:
		if len(import_sessions) > 1:
			bottle.redirect("view/select_import_session")
		else:
			session = import_sessions[0]
			bottle.redirect(f"view/organize_links?session={session}")
	# obviously else
	
	return

# import wizard---------------------------------------------------------------

@bottle.route("/import_wizard")
def import_wizard():
	# display_err_block
	# err_msg
	disp_err = True if err_msg else False
	return bottle.template("view/import_links"
		, err_msg=err_msg
		, display_err_block=disp_err)

@bottle.route("/import_file", method="POST")
def import_file():
	# try:
	#     # parsing
	# except Exception as err_msg:
	#     pass
	if parsing_successful:
		bottle.redirect("/index")
	else:
		bottle.redirect(f"/import_wizard?err={err_msg}")
	return

# run-------------------------------------------------------------------------

if __name__ == '__main__':
	bottle.run(debug=True, reloader=True)
