# Endpoint for temperatures route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from datetime import timezone
from model.historic.HistoricTemperatureModel import HistoricTemperatureModel
import logging
import time
import mariadb

logging.getLogger(__name__)

@app.route('/historic/temperatures', methods=['GET'])
def historic_temperatures_get_all():
	logging.debug("Received request /historic/temperatures")
	startTime = time.monotonic()
	try:
		dataArray = []
		temperatureArray = HistoricTemperatureModel.get_all()
		for tempModel in temperatureArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/temperatures/<int:id>', methods=['GET'])
def historic_temperatures_get_by_id(id):
	logging.debug("Received request /historic/temperatures/<id>")
	startTime = time.monotonic()
	try:
		returnValue = HistoricTemperatureModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get by id request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/temperatures/search', methods=['GET'])
def historic_temperatures_get_by_search():
	logging.debug("Received request /historic/temperatures/search")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		dataArray = []
		temperatureArray = HistoricTemperatureModel.get_by_search(start,end)
		for tempModel in temperatureArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get by search request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/temperatures/oldest', methods=['GET'])
def historic_temperatures_get_oldest():
	logging.debug("Received request /historic/temperatures/oldest")
	startTime = time.monotonic()
	try:
		returnValue = HistoricTemperatureModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get oldest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/temperatures/newest', methods=['GET'])
def historic_temperatures_get_newest():
	logging.debug("Received request /historic/temperatures/newest")
	startTime = time.monotonic()
	try:
		returnValue = HistoricTemperatureModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get newest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/temperatures/average', methods=['GET'])
def historic_temperatures_get_average():
	logging.debug("Received request /historic/temperatures/average")
	startTime = time.monotonic()
	try:
		returnValue = HistoricTemperatureModel.get_average()
		data = HistoricTemperatureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get average request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/temperatures/average/range', methods=['GET'])
def historic_temperatures_get_average_in_range():
	logging.debug("Received request /historic/temperatures/average/range")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = HistoricTemperatureModel.get_average_by_range(start,end)
		data = HistoricTemperatureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get average in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route("/historic/temperatures/reset", methods=["DELETE"])
def historic_temperatures_reset():
	logging.debug("Received request /historic/temperatures/reset")
	startTime = time.monotonic()
	try:
		# Requires a simple pw
		pw = req.args.get("pw")
		if pw != "A7G2V9":
			abort(403)

		HistoricTemperatureModel.delete_all()
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature reset request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/temperatures/reset/range', methods=['DELETE'])
def historic_temperatures_reset_in_range():
	logging.debug("Received request /historic/temperatures/reset/range")
	startTime = time.monotonic()
	try:
		# Requires a simple pw
		pw = req.args.get("pw")
		if pw != "A7G2V9":
			abort(403)

		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		HistoricTemperatureModel.delete_by_range(start,end)
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature reset in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))
