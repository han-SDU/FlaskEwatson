# Module responsible to talk to the co2 sensor hardware
import time
import random
import os
import logging
from model.CO2Model import CO2Model

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
			value = random.uniform(0,69)
			newReading = CO2Model(None,None,value)

			# Insert into db
			logging.info("Generating mock data for co2 sensor with value: "+str(value))
			newReading.post()

			time.sleep(5)
		except BaseException as e:
			logging.exception(e)
			

def collectData():
	raise NotImplementedError
