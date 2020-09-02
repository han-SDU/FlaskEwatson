from model.connectionService import ConnectionService

class TemperatureModel():
	def __init__(self,id,time,value):
		self.id = id
		self.time = time
		self.value = value

	def post(self):
		# Init
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Insert into tbl_temperature(fld_time,fld_value) values (NOW(),?)',(self.value,))
		conn.commit()

		# Update this Object with
		self.id = cur.lastrowid
		self.time = TemperatureModel.get_by_id(self.id).time

		# Clean and return
		conn.close()
		return self.id

	def put(self):
		# Not needing this implementation
		pass

	def to_json(self):
		data = {
			'type': 'Temperature sensor reading',
			'id': self.id,
			'attributes': {
				'value': str(self.value),
				'readingTime': self.time,
				'readingUnit': 'celsius'
				}
			}
		return data

	@staticmethod
	def average_json(avgDecimal):
		json = {
			'type': 'Temperature average',
			'attributes': {
					'average': str(avgDecimal),
					'readingUnit' : 'celsius'
					}
			}
		return json

	@staticmethod
	def delete(id):
		# Not needing this implementation
		pass

	@staticmethod
	def get_by_id(id):
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_temperature where fld_pk_id=?', (id,))

		# Formatting of return data
		for id,time,value in cur:
			returnValue = TemperatureModel(id,time,value)

		# Clean and return
		conn.close()
		return returnValue

	@staticmethod
	def get_all():
		# Init
		returnValue = []
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_temperature')

		# Formatting of return data
		for id,time,value in cur:
			temp = TemperatureModel(id,time,value)
			returnValue.append(temp)

		# Clean and return
		conn.close()
		return returnValue


	@staticmethod
	def get_by_search(start,end):
		# Init
		returnValue = []
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_temperature where fld_time>=? and fld_time<=?', (start,end,))

		# Formatting of return data
		for id,time,value in cur:
			temp = TemperatureModel(id,time,value)
			returnValue.append(temp)

		# Clean and return
		conn.close()
		return returnValue

	@staticmethod
	def get_oldest():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_temperature order by fld_time asc limit 1')

		# Formatting of return data
		for id,time,value in cur:
			returnValue = TemperatureModel(id,time,value)

		# Clean and return
from model.PressureModel import PressureModel
from model.HumidityModel import HumidityModel
from model.CO2Model import CO2Model
from model.TemperatureModel import TemperatureModel

class SensorModel():
	def __init__(self,pressures,humidities,co2,temperatures):
		self.pressures = pressures
		self.humidities = humidities
		self.co2 = co2
		self.temperatures = temperatures

	# Used if container is filled with arrays
	def to_json_array(self):
		# Init
		pressureJsonArray = []
		humidityJsonArray = []
		co2JsonArray = []
		temperatureJsonArray = []

		# Converting to json
		for press in self.pressures:
			pressureJsonArray.append(press.to_json())

		for hum in self.humidities:
			humidityJsonArray.append(hum.to_json())

		for c in self.co2:
			co2JsonArray.append(c.to_json())

		for temp in self.temperatures:
			temperatureJsonArray.append(temp.to_json())

		# Return data
		data = {
			'type': 'All sensor readings',
			'attributes': {
				'pressures': pressureJsonArray,
				'humidities': humidityJsonArray,
				'co2': co2JsonArray,
				'temperatures': temperatureJsonArray
				}
			}
		return data

	# Used if variables are only one value
	def to_single_json(self):
		# Init
		pressureJson = self.pressures.to_json()
		humidityJson = self.humidities.to_json()
		co2Json = self.co2.to_json()
		temperatureJson = self.temperatures.to_json()

		# Return data
		data = {
			'type': 'All sensor readings',
			'attributes': {
				'pressure': pressureJson,
				'humiditie': humidityJson,
				'co2': co2Json,
				'temperature': temperatureJson
				}
			}
		return data

	def to_average_json(self):
		json = {
			'type': 'All sensor average',
			'Attributes': {
				'pressure': PressureModel.average_json(self.pressures),
				'humidity': HumidityModel.average_json(self.humidities),
				'co2': CO2Model.average_json(self.co2),
				'temperature': TemperatureModel.average_json(self.temperatures)
				}
			}
		return json

	# The nuclear option, sending an entire database via json
	@staticmethod
	def get_all():
		# init
		foundPressure = []
		foundHumidities = []
		foundCo2 = []
		foundTemperatures = []

		# Execution (4 connection, could be more effecient but query time is hardly an issue)
		foundPressure = PressureModel.get_all()
		foundHumidities = HumidityModel.get_all()
		foundCo2 = CO2Model.get_all()
		foundTemperatures = TemperatureModel.get_all()

		# Build object
		returnObj = SensorModel(foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj


	@staticmethod
	def get_by_search(start,end):
		# init
		foundPressure = []
		foundHumidities = []
		foundCo2 = []
		foundTemperatures = []

		# Execution (4 connection, could be more effecient but query time is hardly an issue)
		foundPressure = PressureModel.get_by_search(start,end)
		foundHumidities = HumidityModel.get_by_search(start,end)
		foundCo2 = CO2Model.get_by_search(start,end)
		foundTemperatures = TemperatureModel.get_by_search(start,end)

		# Build object
		returnObj = SensorModel(foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

	def get_oldest():
		# init
		foundPressure = None
		foundHumidities = None
		foundCo2 = None
		foundTemperatures = None

		# Execution (4 connection, could be more effecient but query time is hardly an issue)
		foundPressure = PressureModel.get_oldest()
		foundHumidities = HumidityModel.get_oldest()
		foundCo2 = CO2Model.get_oldest()
		foundTemperatures = TemperatureModel.get_oldest()

		# Build object
		returnObj = SensorModel(foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj


	def get_newest():
		# init
		foundPressure = None
		foundHumidities = None
		foundCo2 = None
		foundTemperatures = None

		# Execution (4 connection, could be more effecient but query time is hardly an issue)
		foundPressure = PressureModel.get_newest()
		foundHumidities = HumidityModel.get_newest()
		foundCo2 = CO2Model.get_newest()
		foundTemperatures = TemperatureModel.get_newest()

		# Build object
		returnObj = SensorModel(foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

	def get_average():
		# init
		foundPressure = None
		foundHumidities = None
		foundCo2 = None
		foundTemperatures = None

		# Execution (4 connection, could be more effecient but query time is hardly an issue)
		foundPressure = PressureModel.get_average()
		foundHumidities = HumidityModel.get_average()
		foundCo2 = CO2Model.get_average()
		foundTemperatures = TemperatureModel.get_average()

		# Build object
		returnObj = SensorModel(foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj


	def get_average_by_range():
		# init
		foundPressure = None
		foundHumidities = None
		foundCo2 = None
		foundTemperatures = None

		# Execution (4 connection, could be more effecient but query time is hardly an issue)
		foundPressure = PressureModel.get_average_by_rage(start,end)
		foundHumidities = HumidityModel.get_average_by_range(start,end)
		foundCo2 = CO2Model.get_average_by_range(start,end)
		foundTemperatures = TemperatureModel.get_average_by_range(start,end)

		# Build object
		returnObj = SensorModel(foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

		return returnValue

	@staticmethod
	def get_newest():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_temperature order by fld_time desc limit 1')

		# Formatting of return data
		for id,time,value in cur:
			returnValue = TemperatureModel(id,time,value)

		# Clean and return
		return returnValue

	@staticmethod
	def get_average():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select AVG(fld_value) from tbl_temperature')

		# Formatting of return data
		for c in cur:
			returnValue = c[0] #Average

		# Clean and return
		return returnValue


	@staticmethod
	def get_average_by_range(start,end):
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select AVG(fld_value) from tbl_temperature where fld_time>=? and fld_time<=?', (start,end,))

		# Formatting of return data
		for c in cur:
			returnValue = c[0] #Average

		# Clean and return
		return returnValue
