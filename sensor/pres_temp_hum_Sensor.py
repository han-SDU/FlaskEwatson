# Module responsible to talk to the temperature sensor Hardware
import time
import os
import random
import logging
from smbus2 import SMBus
from model.recent.RecentTemperatureModel import RecentTemperatureModel
from model.recent.RecentPressureModel import RecentPressureModel
from model.recent.RecentHumidityModel import RecentHumidityModel

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
			value = random.uniform(-30,40)
			newReading = TemperatureModel(None,None,value)

			# Save to db
			logging.info("Generating mock data for temperature sensor with value: "+str(value))
			newReading.post()

			time.sleep(5)
		except BaseException as e:
			logging.exception(e)
		

def collectData():
	bus = SMBus(1)

	dT = []
	dP = []
	dH = []

	flo = 0.0


	def writeReg(reg_address, data):
		bus.write_byte_data(0x76,reg_address,data)

	def get_calib_param():
		calib = []
		
		for i in range (0x88,0x88+24):
			calib.append(bus.read_byte_data(0x76,i))
		calib.append(bus.read_byte_data(0x76,0xA1))
		for i in range (0xE1,0xE1+7):
			calib.append(bus.read_byte_data(0x76,i))

		dT.append((calib[1] << 8) | calib[0])
		dT.append((calib[3] << 8) | calib[2])
		dT.append((calib[5] << 8) | calib[4])
		dP.append((calib[7] << 8) | calib[6])
		dP.append((calib[9] << 8) | calib[8])
		dP.append((calib[11]<< 8) | calib[10])
		dP.append((calib[13]<< 8) | calib[12])
		dP.append((calib[15]<< 8) | calib[14])
		dP.append((calib[17]<< 8) | calib[16])
		dP.append((calib[19]<< 8) | calib[18])
		dP.append((calib[21]<< 8) | calib[20])
		dP.append((calib[23]<< 8) | calib[22])
		dH.append( calib[24] )
		dH.append((calib[26]<< 8) | calib[25])
		dH.append( calib[27] )
		dH.append((calib[28]<< 4) | (0x0F & calib[29]))
		dH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
		dH.append( calib[31] )
		
		for i in range(1,2):
			if dT[i] & 0x8000:
				dT[i] = (-dT[i] ^ 0xFFFF) + 1

		for i in range(1,8):
			if dP[i] & 0x8000:
				dP[i] = (-dP[i] ^ 0xFFFF) + 1

		for i in range(0,6):
			if dH[i] & 0x8000:
				dH[i] = (-dH[i] ^ 0xFFFF) + 1  

	def readData():
		data = []
		for i in range (0xF7, 0xF7+8):
			data.append(bus.read_byte_data(0x76,i))
		pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
		temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
		hum_raw  = (data[6] << 8)  |  data[7]
		
		comp_T(temp_raw)
		comp_P(pres_raw)
		comp_H(hum_raw)

	def comp_P(adc_pres):
		global  flo
		pressure = 0.0
		
		v1 = (flo / 2.0) - 64000.0
		v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * dP[5]
		v2 = v2 + ((v1 * dP[4]) * 2.0)
		v2 = (v2 / 4.0) + (dP[3] * 65536.0)
		v1 = (((dP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((dP[1] * v1) / 2.0)) / 262144
		v1 = ((32768 + v1) * dP[0]) / 32768
		
		if v1 == 0:
			return 0
		pressure = ((1048576 - adc_pres) - (v2 / 4096)) * 3125
		if pressure < 0x80000000:
			pressure = (pressure * 2.0) / v1
		else:
			pressure = (pressure / v1) * 2
		v1 = (dP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
		v2 = ((pressure / 4.0) * dP[7]) / 8192.0
		pressure = pressure + ((v1 + v2 + dP[6]) / 16.0)  
		pressure = pressure/100 #converts to hPa
		
		# Save to db
		newReading = RecentPressureModel(None,None,pressure)
		logging.info("Reading pressure sensor with value: "+str(pressure))
		newReading.post()

	def comp_T(adc_temp):
		global flo
		v1 = (adc_temp / 16384.0 - dT[0] / 1024.0) * dT[1]
		v2 = (adc_temp / 131072.0 - dT[0] / 8192.0) * (adc_temp / 131072.0 - dT[0] / 8192.0) * dT[2]
		flo = v1 + v2
		temperature = flo / 5120.0
		#print "temp : %-6.2f " % (temperature) 
		
		# Save to db
		newReading = RecentTemperatureModel(None,None,temperature)
		logging.info("Reading temperature sensor with value: "+str(temperature))
		newReading.post()

	def comp_H(adc_hum):
		global flo
		humidity = flo - 76800.0
		if humidity != 0:
			humidity = (adc_hum - (dH[3] * 64.0 + dH[4]/16384.0 * humidity)) * (dH[1] / 65536.0 * (1.0 + dH[5] / 67108864.0 * humidity * (1.0 + dH[2] / 67108864.0 * humidity)))
		else:
			return 0
		humidity = humidity * (1.0 - dH[0] * humidity / 524288.0)
		if humidity > 100.0:
			humidity = 100.0
		elif humidity < 0.0:
			humidity = 0.0
		#print "hum : %6.2f" % (humidity)
		
		# Save to db
		newReading = RecentHumidityModel(None,None,humidity)
		logging.info("Reading humidity sensor with value: "+str(humidity))
		newReading.post()


	def setup():
		osrs_t = 1			#Temperature oversampling x 1
		osrs_p = 1			#Pressure oversampling x 1
		osrs_h = 1			#Humidity oversampling x 1
		mode   = 3			
		t_sb   = 5			
		filter = 0			
		spi3w_en = 0		

		ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
		config_reg    = (t_sb << 5) | (filter << 2) | spi3w_en
		ctrl_hum_reg  = osrs_h

		writeReg(0xF2,ctrl_hum_reg)
		writeReg(0xF4,ctrl_meas_reg)
		writeReg(0xF5,config_reg)


	setup()
	get_calib_param()
	
	while True:
		try:
			readData()
		except KeyboardInterrupt:
			pass
		time.sleep(5)
		
