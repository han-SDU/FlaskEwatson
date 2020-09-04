# Module responsible to talk to the humidity sensor hardware
import time
import os
import random
from model.HumidityModel import HumidityModel

def run():
	if os.environ.get("DEVELOPMENT") == "1":
		mockRun()
	else:
		collectData()

def mockRun():
	while True:
		# Create a Mock value
		value = random.uniform(0,100)
		newReading = HumidityModel(None, None, value)

		# Place in database
		print("Generating mock data for humidity sensor with value: "+str(value))
		newReading.post()

		time.sleep(5)

def collectData():
	raise NotImplementedError

