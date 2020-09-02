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
		newReading.post()

		time.sleep(5)

