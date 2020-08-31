# Main entry point for the server application
from flask import Flask
from flask import request as req
from datetime import datetime
from flask_json import FlaskJSON
from flask_json import json_response as res

#Globals
ip = 1
port = 5000

#Start up
app = Flask(__name__)
FlaskJSON(app)

#Other routes, each endpoint should get its own file
from api import sensors
from api import temperatures
from api import CO2
from api import humidities

#config for running dev, havent looked at prod server yet
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
