# Module responsible to talk to the humidity sensor hardware
import time
import random
from model.HumidityModel import HumidityModel

def run():
	while True:
		# Create a Mock value
		value = random.uniform(0,100)
		newReading = HumidityModel(None, None, value)

		# Place in database
		print("Generating mock data for humidity sensor with value: "+str(value))
		newReading.post()

		time.sleep(5)

