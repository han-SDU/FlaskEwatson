import threading
import sys
import getopt
import os
import argparse
import logging
import logging.handlers as handlers
from threading import Event
from server import server
from sensor import temperatureSensor
from sensor import pressureSensor
from sensor import humiditySensor
from sensor import co2Sensor

# Main entry point of application
def main(argv):
	# Parsing argv
	parser = argparse.ArgumentParser()

	parser.add_argument("-d","--development", help="Sets runtime enviroment",action="store_true", dest="development")
	parser.add_argument("-cll","--consolLoglevel", help="Sets verbosity of consol logging" ,choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"],default="WARNING",action="store",dest="consolLogLevel")
	parser.add_argument("-fll","--fileLoglevel", help="Sets verbosity of file logging" ,choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"],default="WARNING",action="store",dest="fileLogLevel")

	args = parser.parse_args()

	try:
		# Setting up logger
		logFormatter = logging.Formatter("%(asctime)s %(levelname)-8s %(threadName)-25s %(module)-25s %(message)s")
		rootLogger = logging.getLogger()
		rootLogger.setLevel(logging.DEBUG)

		# Consol handler
		consolLogger = logging.StreamHandler()
		consolLogger.setLevel(args.consolLogLevel)
		consolLogger.setFormatter(logFormatter)
		rootLogger.addHandler(consolLogger)

		# File handler
		fileLogger = handlers.RotatingFileHandler(filename="logging/logging.log",maxBytes=10*1024*1024,backupCount=5)
		fileLogger.setLevel(args.fileLogLevel)
		fileLogger.setFormatter(logFormatter)
		rootLogger.addHandler(fileLogger)

		# Setting up runtime enviroment
		logging.info("Application started")
		if args.development == True:
			logging.info("Application started in DEVELOPMENT mode")
			os.environ["DEVELOPMENT"]="1"

		# Sensor related start up
		logging.info('Starting Temperature Sensor')
		temperatureDaemon = threading.Thread(target=temperatureSensor.run, daemon=True)
		temperatureDaemon.name = "TemperatureDaemon"
		temperatureDaemon.start()

		logging.info('Starting Pressure Sensor')
		pressureDaemon = threading.Thread(target=pressureSensor.run, daemon=True)
		pressureDaemon.name = "PressureDaemon"
		pressureDaemon.start()

		logging.info('Starting Humidity Sensor')
		humidityDaemon = threading.Thread(target=humiditySensor.run, daemon=True)
		humidityDaemon.name = "HumidityDaemon"
		humidityDaemon.start()

		logging.info('Starting CO2 Sensor')
		co2Daemon = threading.Thread(target=co2Sensor.run, daemon=True)
		co2Daemon.name = "CO2Daemon"
		co2Daemon.start()

		# Http related start up
		logging.info('Starting Flask Server')
		serverDaemon = threading.Thread(target=server.run, daemon=True)
		serverDaemon.name = "ServerDaemon"
		serverDaemon.start()

		Event().wait()
		logging.info('Exit with ctrl-c')
	except KeyboardInterrupt as e:
		logging.info('Shutting down')
	except BaseException as e:
		logging.exception(e)

	# Add a catch all
if __name__=="__main__":
	main(sys.argv[1:])
