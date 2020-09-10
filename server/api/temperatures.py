# Endpoint for temperatures route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.TemperatureModel import TemperatureModel
import logging
import time
import mariadb

logging.getLogger(__name__)

@app.route('/temperatures', methods=['GET'])
def temperatures_get_all():
	logging.debug("Recived request /temperatures")
	startTime = time.monotonic()
	try:
		dataArray = []
		temperatureArray = TemperatureModel.get_all()
		for tempModel in temperatureArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/<int:id>', methods=['GET'])
def temperatures_get_by_id(id):
	logging.debug("Recived request /temperatures/<id>")
	startTime = time.monotonic()
	try:
		returnValue = TemperatureModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get by id request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/search', methods=['GET'])
def temperatures_get_by_search():
	logging.debug("Recived request /temperatures/search")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		dataArray = []
		temperatureArray = TemperatureModel.get_by_search(start,end)
		for tempModel in temperatureArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get by search request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/oldest', methods=['GET'])
def temperatures_get_oldest():
	logging.debug("Recived request /temperatures/oldest")
	startTime = time.monotonic()
	try:
		returnValue = TemperatureModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get oldest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/newest', methods=['GET'])
def temperatures_get_newest():
	logging.debug("Recived request /temperatures/newest")
	startTime = time.monotonic()
	try:
		returnValue = TemperatureModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get newest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/average', methods=['GET'])
def temperatures_get_average():
	logging.debug("Recived request /temperatures/average")
	startTime = time.monotonic()
	try:
		returnValue = TemperatureModel.get_average()
		data = TemperatureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get average request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/average/range', methods=['GET'])
def temperatures_get_average_in_range():
	logging.debug("Recived request /temperatures/average/range")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = TemperatureModel.get_average_by_range(start,end)
		data = TemperatureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get average in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))
