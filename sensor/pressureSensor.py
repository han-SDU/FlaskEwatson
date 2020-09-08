# Module responsible to talk to the pressure sensor hardware
import time
import os
import random
import logging
from model.PressureModel import PressureModel

logger = logging.getLogger(__name__)

def run():
	if os.environ.get("DEVELOPMENT") == "1":
		mockRun()
	else:
		collectData()

def mockRun():
	while True:
		# Mock data creation
		value = random.uniform(0,100)
		newReading = PressureModel(None,None,value)

		# Insert
		logger.info("Generating mock data for pressure sensor with value: "+str(value))
		newReading.post()

		time.sleep(5)

def collectData():
	raise NotImplementedError

