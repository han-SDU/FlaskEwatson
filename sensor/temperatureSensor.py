# Module responsible to talk to the temperature sensor Hardware
import time
import os
import random
from model.TemperatureModel import TemperatureModel

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
		print("Generating mock data for temperature sensor with value: "+str(value))
		newReading.post()

		time.sleep(5)

def collectData():
	raise NotImplementedError
