# Module responsible to talk to the co2 sensor hardware
import time
import random
from model.CO2Model import CO2Model

def run():
	while True:
		# Create Mock data
		value = random.uniform(0,69)
		newReading = CO2Model(None,None,value)

		# Insert into db
		print("Generating mock data for co2 sensor with value: "+str(value))
		newReading.post()

		time.sleep(5)

