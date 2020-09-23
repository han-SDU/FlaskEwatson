# Module responsible to talk to the humidity sensor hardware
import time
import os
import random
import logging
from model.recent.RecentHumidityModel import RecentHumidityModel

logging.getLogger(__name__)

def run():
	if os.environ.get("DEVELOPMENT") == "1":
		mockRun()
	else:
		collectData()

def mockRun():
	while True:
		try:
			# Create a Mock value
			value = random.uniform(0,100)
			newReading = RecentHumidityModel(None, None, value)

			# Place in database
			logging.info("Generating mock data for humidity sensor with value: "+str(value))
			newReading.post()

			time.sleep(5)
		except BaseException as e:
			logging.exception(e)

def collectData():
	raise NotImplementedError

