# Main entry point for the server application
from flask import Flask
from flask import url_for
from flask import request as req
from datetime import datetime
from flask_json import FlaskJSON
from flask_json import json_response as res
from flask_cors import CORS
import traceback

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
FlaskJSON(app)
CORS(app)

#Other routes, each endpoint should get its own file	from server.api import sensors
from server.api import temperatures
from server.api import CO2
from server.api import humidities
from server.api import pressures
from server.api import sensors

# Error Handlers for app
@app.errorhandler(403)
def handler_403(e):
	return res(403, error=str(e), time=datetime.utcnow())

@app.errorhandler(404)
def handler_404(e):
	return res(404, error=str(e), time=datetime.utcnow())

@app.errorhandler(405)
def handler_405(e):
	return res(405, error=str(e), time=datetime.utcnow())

@app.errorhandler(500)
def handler_500(e):
	traceback.print_exc()
	return res(500, error=str(e), time=datetime.utcnow())

@app.errorhandler(501)
def handler_501(e):
	return res(501, error=str(e), time=datetime.utcnow())

@app.errorhandler(Exception)
def handler_default(e):
	traceback.print_exc()
	return res(500, error=str(e), time=datetime.utcnow())


#Start up
def run():
	#config for running dev, havent looked at prod server yet
	app.run(debug=False, host='0.0.0.0', port=5000)
