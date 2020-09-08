# Module responsible to talk to the temperature sensor Hardware
import time
import os
import random
import logging
from model.TemperatureModel import TemperatureModel

logger = logging.getLogger(__name__)

def run():
	if os.environ.get("DEVELOPMENT") == "1":
		mockRun()
	else:
		collectData()

def mockRun():
	while True:
		# Create Mock data
		value = random.uniform(-30,40)
		newReading = TemperatureModel(None,None,value)

		# Save to db
		logger.info("Generating mock data for temperature sensor with value: "+str(value))
		newReading.post()

		time.sleep(5)

def collectData():
	raise NotImplementedError
