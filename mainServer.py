import threading
import sys
import getopt
import os
import argparse
import logging
import logging.handlers as handlers
from threading import Event
from flask import Flask
from flask import url_for
from flask import request as req
from datetime import datetime
from flask_json import FlaskJSON
from flask_json import json_response as res
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
FlaskJSON(app)
CORS(app)

from server.handlers import error_handler_api
from server.api.base import base_api

from server.api.historic.historicCO2 import historic_co2_api
from server.api.historic.historicHumidities import historic_humidities_api
from server.api.historic.historicPressures import historic_pressures_api
from server.api.historic.historicSensors import historic_sensors_api
from server.api.historic.historicTemperatures import historic_temperatures_api

from server.api.recent.recentCO2 import recent_co2_api
from server.api.recent.recentHumidities import recent_humidities_api
from server.api.recent.recentPressures import recent_pressures_api
from server.api.recent.recentSensors import recent_sensors_api
from server.api.recent.recentTemperatures import recent_temperatures_api

app.register_blueprint(error_handler_api)
app.register_blueprint(base_api)

app.register_blueprint(historic_co2_api, url_prefix="/historic/co2")
app.register_blueprint(historic_humidities_api, url_prefix="/historic/humidities")
app.register_blueprint(historic_pressures_api, url_prefix="/historic/pressures")
app.register_blueprint(historic_sensors_api, url_prefix="/historic/sensors")
app.register_blueprint(historic_temperatures_api, url_prefix="/historic/temperatures")

app.register_blueprint(recent_co2_api, url_prefix="/recent/co2")
app.register_blueprint(recent_humidities_api, url_prefix="/recent/humidities")
app.register_blueprint(recent_pressures_api, url_prefix="/recent/pressures")
app.register_blueprint(recent_sensors_api, url_prefix="/recent/sensors")
app.register_blueprint(recent_temperatures_api, url_prefix="/recent/temperatures")

def main(argv):
    # Parsing argv
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Sets debugging on server", type=bool, default=False, action="store", dest="debug")
    
    parser.add_argument("--host", help="Sets the host", type=str, default='0.0.0.0', action="store", dest="host")
                        
    parser.add_argument("-p", "--port", help="Sets the port", type=int, default=5000, action="store", dest="port")
    
    parser.add_argument("-cll", "--consolLoglevel", help="Sets verbosity of consol logging", choices=[
                        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO", action="store", dest="consolLogLevel")
    
    parser.add_argument("-fll", "--fileLoglevel", help="Sets verbosity of file logging", choices=[
                        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="WARNING", action="store", dest="fileLogLevel")
    
    parser.add_argument("-fo", "--fileOutput", help="File name of logging file", type=str, default="logging", action="store", dest="logFileName")

    args = parser.parse_args()

    try:
        # Setting up logger
        logFormatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(threadName)-25s %(module)-25s %(message)s")
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.DEBUG)

        # Consol handler
        consolLogger = logging.StreamHandler()
        consolLogger.setLevel(args.consolLogLevel)
        consolLogger.setFormatter(logFormatter)
        rootLogger.addHandler(consolLogger)

        # File handler
        if not os.path.exists('logging'):
            os.makedirs('logging')
        if not os.path.exists('logging/server'):
            os.makedirs('logging/server')
        fileLogger = handlers.RotatingFileHandler(
            filename="logging/server/"+args.logFileName+".log", maxBytes=10*1024*1024, backupCount=5)
        fileLogger.setLevel(args.fileLogLevel)
        fileLogger.setFormatter(logFormatter)
        rootLogger.addHandler(fileLogger)

        # Setting up runtime environment
        logging.info("Application started")

        # Echo other configs
        logging.info("Consol log level: " + args.consolLogLevel)
        logging.info("File log level: " + args.fileLogLevel)
        logging.info("File logging output: logging/"+args.logFileName+".log")

        app.run(debug=args.debug, host=args.host, port= args.port)

        Event().wait()
        logging.info('Exit with ctrl-c')
    except KeyboardInterrupt as e:
        logging.info('Shutting down')
    except BaseException as e:
        logging.exception(e)

    # Add a catch all
if __name__ == "__main__":
    try:
	    main(sys.argv[1:])
    except BaseException as e:
        logging.exception(e)

