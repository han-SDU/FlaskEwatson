import threading
import sys
import getopt
import os
import logging
from threading import Event
from server import server
from sensor import temperatureSensor
from sensor import pressureSensor
from sensor import humiditySensor
from sensor import co2Sensor

# Main entry point of application
def main(argv):
	try:
		logging.basicConfig(
			level=logging.DEBUG,
			format="[%(levelname)s][%(asctime)s] %(threadName)s [%(module)s]: %(message)s",
			handlers=[
				logging.FileHandler("logging.log"),
				logging.StreamHandler()
			]
		)

		# Parsing argv
		opts, args = getopt.getopt(argv,"-d","--development")
		for opt, arg in opts:
			if opt == "-d":
				os.environ["DEVELOPMENT"] = "1"

		logging.info("Application started")
		if os.environ.get("DEVELOPMENT") == "1":
			logging.info("Application started in DEVELOPMENT mode")

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
