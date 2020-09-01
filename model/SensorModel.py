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

	def to_json(self):
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
			'type': 'All Sensor readings',
			'attributes': {
				'pressures': pressureJsonArray,
				'humidities': humidityJsonArray,
				'co2': co2JsonArray,
				'temperatures': temperatureJsonArray
				}
			}
		return data

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

