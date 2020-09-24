from model.historic.HistoricPressureModel import HistoricPressureModel
from model.historic.HistoricHumidityModel import HistoricHumidityModel
from model.historic.HistoricCO2Model import HistoricCO2Model
from model.historic.HistoricTemperatureModel import HistoricTemperatureModel
import logging

logging.getLogger(__name__)


class HistoricSensorModel():
	def __init__(self, pressures, humidities, co2, temperatures):
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
			'type': 'All historic sensor readings',
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
		pressureJson = None
		humidityJson = None
		co2Json = None
		temperatureJson = None

		if self.pressures is not None:
			pressureJson = self.pressures.to_json()

		if self.humidities is not None:
			humidityJson = self.humidities.to_json()

		if self.co2 is not None:
			co2Json = self.co2.to_json()

		if self.temperatures is not None:
			temperatureJson = self.temperatures.to_json()

		# Return data
		logging.debug("Formatting SensorModel to json")
		data = {
			'type': 'All historic sensor readings',
			'attributes': {
				'pressure': pressureJson,
				'humidity': humidityJson,
				'co2': co2Json,
				'temperature': temperatureJson
			}
		}
		return data

	def to_average_json(self):
		logging.debug("Formatting SensorModel to average json")
		json = {
			'type': 'All historic sensor average',
			'attributes': {
				'pressure': HistoricPressureModel.average_json(self.pressures),
				'humidity': HistoricHumidityModel.average_json(self.humidities),
				'co2': HistoricCO2Model.average_json(self.co2),
				'temperature': HistoricTemperatureModel.average_json(self.temperatures)
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

		# Execution (4 connection, could be more efficient but query time is hardly an issue)
		foundPressure = HistoricPressureModel.get_all()
		foundHumidities = HistoricHumidityModel.get_all()
		foundCo2 = HistoricCO2Model.get_all()
		foundTemperatures = HistoricTemperatureModel.get_all()

		# Build object
		returnObj = HistoricSensorModel(
			foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

	@staticmethod
	def get_by_search(start, end):
		# init
		foundPressure = []
		foundHumidities = []
		foundCo2 = []
		foundTemperatures = []

		# Execution (4 connection, could be more efficient but query time is hardly an issue)
		foundPressure = HistoricPressureModel.get_by_search(start, end)
		foundHumidities = HistoricHumidityModel.get_by_search(start, end)
		foundCo2 = HistoricCO2Model.get_by_search(start, end)
		foundTemperatures = HistoricTemperatureModel.get_by_search(start, end)

		# Build object
		returnObj = HistoricSensorModel(
			foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

	@staticmethod
	def get_oldest():
		# init
		foundPressure = None
		foundHumidities = None
		foundCo2 = None
		foundTemperatures = None

		# Execution (4 connection, could be more efficient but query time is hardly an issue)
		foundPressure = HistoricPressureModel.get_oldest()
		foundHumidities = HistoricHumidityModel.get_oldest()
		foundCo2 = HistoricCO2Model.get_oldest()
		foundTemperatures = HistoricTemperatureModel.get_oldest()

		# Build object
		returnObj = HistoricSensorModel(
			foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

	@staticmethod
	def get_newest():
		# init
		foundPressure = None
		foundHumidities = None
		foundCo2 = None
		foundTemperatures = None

		# Execution (4 connection, could be more efficient but query time is hardly an issue)
		foundPressure = HistoricPressureModel.get_newest()
		foundHumidities = HistoricHumidityModel.get_newest()
		foundCo2 = HistoricCO2Model.get_newest()
		foundTemperatures = HistoricTemperatureModel.get_newest()

		# Build object
		returnObj = HistoricSensorModel(
			foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

	@staticmethod
	def get_average():
		# init
		foundPressure = None
		foundHumidities = None
		foundCo2 = None
		foundTemperatures = None

		# Execution (4 connection, could be more efficient but query time is hardly an issue)
		foundPressure = HistoricPressureModel.get_average()
		foundHumidities = HistoricHumidityModel.get_average()
		foundCo2 = HistoricCO2Model.get_average()
		foundTemperatures = HistoricTemperatureModel.get_average()

		# Build object
		returnObj = HistoricSensorModel(
			foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

	@staticmethod
	def get_average_by_range(start, end):
		# init
		foundPressure = None
		foundHumidities = None
		foundCo2 = None
		foundTemperatures = None

		# Execution (4 connection, could be more efficient but query time is hardly an issue)
		foundPressure = HistoricPressureModel.get_average_by_range(start, end)
		foundHumidities = HistoricHumidityModel.get_average_by_range(start, end)
		foundCo2 = HistoricCO2Model.get_average_by_range(start, end)
		foundTemperatures = HistoricTemperatureModel.get_average_by_range(start, end)

		# Build object
		returnObj = HistoricSensorModel(
			foundPressure, foundHumidities, foundCo2, foundTemperatures)

		# Clean and return
		return returnObj

	@staticmethod
	def delete_all():
		# Init
		returnValue = True

		# Execution
		HistoricPressureModel.delete_all()
		HistoricHumidityModel.delete_all()
		HistoricCO2Model.delete_all()
		HistoricTemperatureModel.delete_all()

		# Clean and return
		return returnValue

	@staticmethod
	def delete_by_range(start, end):
		# Init
		returnValue = True

		# Execution
		HistoricPressureModel.delete_by_range(start, end)
		HistoricHumidityModel.delete_by_range(start, end)
		HistoricCO2Model.delete_by_range(start, end)
		HistoricTemperatureModel.delete_by_range(start, end)

		# Clean and return
		return returnValue
