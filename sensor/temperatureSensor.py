# Module responsible to talk to the temperature sensor Hardware
import time
import os
import random
import logging
from model.recent.RecentTemperatureModel import RecentTemperatureModel

logging.getLogger(__name__)

def run():
	if os.environ.get("DEVELOPMENT") == "1":
		mockRun()
	else:
		collectData()

def mockRun():
	while True:
		try:
			# Create Mock data
			value = random.uniform(-30,40)
			newReading = RecentTemperatureModel(None,None,value)

			# Save to db
			logging.info("Generating mock data for temperature sensor with value: "+str(value))
			newReading.post()

			time.sleep(5)
		except BaseException as e:
			logging.exception(e)
		

def collectData():
	raise NotImplementedError
