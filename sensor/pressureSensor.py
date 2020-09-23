# Module responsible to talk to the pressure sensor hardware
import time
import os
import random
import logging
from model.recent.RecentPressureModel import RecentPressureModel

logging.getLogger(__name__)

def run():
	if os.environ.get("DEVELOPMENT") == "1":
		mockRun()
	else:
		collectData()

def mockRun():
	while True:
		try:
			# Mock data creation
			value = random.uniform(0,100)
			newReading = RecentPressureModel(None,None,value)

			# Insert
			logging.info("Generating mock data for pressure sensor with value: "+str(value))
			newReading.post()

			time.sleep(5)
		except BaseException as e:
			logging.exception(e)
		

def collectData():
	raise NotImplementedError

