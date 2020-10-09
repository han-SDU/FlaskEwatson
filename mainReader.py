import threading
import sys
import getopt
import os
import argparse
import logging
import logging.handlers as handlers
from threading import Event
from sensor import co2Sensor
from sensor import pres_temp_hum_Sensor

# Main entry point of application


def main(argv):
    # Parsing argv
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--development", help="Sets runtime environment",
                        action="store_true", dest="development")
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
        if not os.path.exists('logging/reading'):
            os.makedirs('logging/reading')
        fileLogger = handlers.RotatingFileHandler(
            filename="logging/reading/"+args.logFileName+".log", maxBytes=10*1024*1024, backupCount=5)
        fileLogger.setLevel(args.fileLogLevel)
        fileLogger.setFormatter(logFormatter)
        rootLogger.addHandler(fileLogger)

        # Setting up runtime environment
        logging.info("Application started")
        if args.development == True:
            logging.info("Application started in DEVELOPMENT mode")
            os.environ["DEVELOPMENT"] = "1"

        # Echo other configs
        logging.info("Consol log level: " + args.consolLogLevel)
        logging.info("File log level: " + args.fileLogLevel)
        logging.info("File logging output: logging/"+args.logFileName+".log")

        # Sensor related start up
        logging.info('Starting PTH Sensor')
        PTHDaemon = threading.Thread(
            target=pres_temp_hum_Sensor.run, daemon=True)
        PTHDaemon.name = "PTHDaemon"
        PTHDaemon.start()

        logging.info('Starting CO2 Sensor')
        co2Daemon = threading.Thread(target=co2Sensor.run, daemon=True)
        co2Daemon.name = "CO2Daemon"
        co2Daemon.start()

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
