# Module responsible to talk to the temperature sensor Hardware
import time
import random
from model.TemperatureModel import TemperatureModel

def run():
	while True:
		# Create Mock data
		value = random.uniform(-30,40)
		newReading = TemperatureModel(None,None,value)

		# Save to db
		newReading.post()

		time.sleep(5)
