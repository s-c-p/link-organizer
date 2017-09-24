import bottle

@bottle.route("/")
def index():
	# organized_count
	# pending_count
	# errors_count
	# **** tag_cloud
	# **** project_cloud
	return bottle.template("view/index")

@bottle.route("/search")
def search():
	return




@bottle.route("/view_links")
def view_links():
	return







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

if __name__ == '__main__':
	bottle.run(debug=True, reloader=True)
