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

import server.handlers 
import server.api.base

import server.api.historic.historicCO2
import server.api.historic.historicHumidities
import server.api.historic.historicPressures
import server.api.historic.historicSensors
import server.api.historic.historicTemperatures

import server.api.recent.recentCO2
import server.api.recent.recentHumidities
import server.api.recent.recentPressures
import server.api.recent.recentSensors
import server.api.recent.recentTemperatures

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

