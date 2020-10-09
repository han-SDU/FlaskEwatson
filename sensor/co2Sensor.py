# Module responsible to talk to the co2 sensor hardware
import time
import random
import os
import logging
from model.recent.RecentCO2Model import RecentCO2Model

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
	#!/usr/bin/python
	import math, struct, array, time, io, fcntl


	class i2c(object):
		def __init__(self, device, bus):
			# define bus
			self.fr = io.open("/dev/i2c-1", "rb", buffering=0)
			self.fw = io.open("/dev/i2c-1", "wb", buffering=0)

			# set slave address
			fcntl.ioctl(self.fr, 0x0703, device)
			fcntl.ioctl(self.fw, 0x0703, device)

		def write(self, bytes):
			self.fw.write(bytes)

		def read(self, bytes):
			return self.fr.read(bytes)

		def close(self):
			self.fw.close()
			self.fr.close()

	class T6713(object):
		def __init__(self):
			self.dev = i2c(0x15, 1)

		def gasPPM(self):
			buffer = array.array('B', [0x04, 0x13, 0x8b, 0x00, 0x01])
			self.dev.write(buffer)
			time.sleep(0.1)
			data = self.dev.read(4)
			buffer = array.array('B', data)
			return buffer[2]*256+buffer[3]
			
	while True:
		try:
			# Collect sensor data
			obj = T6713()
			value = obj.gasPPM()
			#print "PPM: ", value
			newReading = CO2Model(None,None,value)

			# Insert into db
			logging.info("Collected co2 sensor data with value: "+str(value))
			newReading.post()

			time.sleep(5)
		except BaseException as e:
			logging.exception(e)
