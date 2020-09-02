# Module responsible to talk to the pressure sensor hardware
import time
import random
from model.PressureModel import PressureModel

def run():
	while True:
		# Mock data creation
		value = random.uniform(0,100)
		newReading = PressureModel(None,None,value)

		# Insert
		newReading.post()

		time.sleep(5)
