import bottle

@bottle.route("/")
def index():
    # organized_count
    # pending_count
    # errors_count
    return bottle.template("view/index")

@bottle.route("/import_wizard")
def import_wizard():
    # display_err_block
    # err_msg
    disp_err = True if err_msg else False
    return bottle.template("view/")

if __name__ == '__main__':
    bottle.run(debug=True, reloader=True)
