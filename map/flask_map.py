"""
Very simple Flask web site, with one page
displaying a course schedule.  We pre-process the 
input file to set correct dates and highlight the 
current week (if the academic term is in session). 

"""



import flask
import logging
#import arrow      # Replacement for datetime, based on moment.js

# Our own modules
import pre        # Preprocess schedule file
import config     # Configure from configuration files or command line


###
# Globals
###
"""
if __name__ == "__main__":
    configuration = config.configuration()
else:
    # If we aren't main, the command line doesn't belong to us
    configuration = config.configuration(proxied=True)
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.api_key = configuration.APE_KEY


if configuration.DEBUG:
    app.logger.setLevel(logging.INFO)
"""
if __name__ == "__main__":
    configuration = config.configuration()
else:
    configuration = config.configuration(proxied=True)

app = flask.Flask(__name__)
CONFIG = config.configuration()
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.INFO) ##Used to be .DEBUG
#app.secret_key=CONFIG.SECRET_KEY

app.api_key = CONFIG.API_KEY
# Pre-processed schedule is global, so be careful to update
# it atomically in the view functions. 
#


###
# Pages
# Each of these transmits the default "200/OK" header
# followed by html from the template.
###

@app.route("/")
@app.route("/index")
def index():
  """Main application page; most users see only this"""
  app.logger.debug("Main page entry")
  pois = pre.process(open(configuration.POI))
  data = {"pois":pois}
  logging.info ("This is pois: {}".format(pois))
  flask.g.pois = pois
  flask.g.api_key = app.api_key
  return flask.render_template('map_marker.html')

@app.route("/refresh")
def refresh():
    """Admin user (or debugger) can use this to reload the schedule."""
    app.logger.debug("Refreshing schedule")
    #global pois
    pois = pre.process(open(configuration.POI))
    return flask.redirect(flask.url_for("index"))


@app.route("/_poi")
def mark_pois():
	"""
	Use flask to send the pois information to the html page.
	"""
	pois = pre.process(open(configuration.POI))
	result = {"pois":pois}
	return flask.jsonify(result = result)
	
	

### Error pages ###
#   Each of these transmits an error code in the transmission
#   header along with the appropriate page html in the
#   transmission body

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.g.linkback =  flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def i_am_busted(error):
    app.logger.debug("500: Server error")
    return flask.render_template('500.html'), 500

@app.errorhandler(403)
def no_you_cant(error):
    app.logger.debug("403: Forbidden")
    return flask.render_template('403.html'), 403

"""
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"
"""

#    
# If run as main program (not under gunicorn), we
# turn on debugging and restrict connections
# to localhost (127.0.0.1)
#
if __name__ == "__main__":
    app.run(port=configuration.PORT, host="127.0.0.1")


