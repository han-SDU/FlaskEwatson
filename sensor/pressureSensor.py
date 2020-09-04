# Module responsible to talk to the pressure sensor hardware
import time
import os
import random
from model.PressureModel import PressureModel

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
		print("Generating mock data for pressure sensor with value: "+str(value))
		newReading.post()

		time.sleep(5)

def collectData():
	raise NotImplementedError

