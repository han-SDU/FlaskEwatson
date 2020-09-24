# Endpoint for humidity route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.HumidityModel import HumidityModel
import logging
import time
import mariadb

logging.getLogger(__name__)

@app.route('/humidities', methods=['GET'])
def humidity_get_all():
	logging.debug("Received request /humidities")
	startTime = time.monotonic()
	try:
		dataArray = []
		humArray = HumidityModel.get_all()
		for tempModel in humArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.isoformat())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/<int:id>', methods=['GET'])
def humidity_get_by_id(id):
	logging.debug("Received request /humidities/<id>")
	startTime = time.monotonic()
	try:
		returnValue = HumidityModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get by id request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/search', methods=['GET'])
def humidity_get_by_search():
	logging.debug("Received request /humidities/search")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		dataArray = []
		humArray = HumidityModel.get_by_search(start,end)
		for tempModel in humArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get by search request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/oldest', methods=['GET'])
def humidity_get_oldest():
	logging.debug("Received request /humidities/oldest")
	startTime = time.monotonic()
	try:
		returnValue = HumidityModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get oldest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/newest', methods=['GET'])
def humidity_get_newest():
	logging.debug("Received request /humidities/newest")
	startTime = time.monotonic()
	try:
		returnValue = HumidityModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get newest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/average', methods=['GET'])
def humidity_get_average():
	logging.debug("Received request /humidities/average")
	startTime = time.monotonic()
	try:
		returnValue = HumidityModel.get_average()
		data = HumidityModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get average request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/average/range', methods=['GET'])
def humidity_get_average_in_range():
	logging.debug("Received request /humidities/average/range")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = HumidityModel.get_average_by_range(start,end)
		data = HumidityModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get average in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))


