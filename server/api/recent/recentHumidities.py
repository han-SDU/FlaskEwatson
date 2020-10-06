# Endpoint for humidity route
from __main__ import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.recent.RecentHumidityModel import RecentHumidityModel
import logging
import time
import mariadb

logging.getLogger(__name__)

@app.route('/recent/humidities', methods=['GET'])
def recent_humidity_get_all():
	logging.debug("Received request /recent/humidities")
	startTime = time.monotonic()
	try:
		dataArray = []
		humArray = RecentHumidityModel.get_all()
		for tempModel in humArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/humidities/<int:id>', methods=['GET'])
def recent_humidity_get_by_id(id):
	logging.debug("Received request /recent/humidities/<id>")
	startTime = time.monotonic()
	try:
		returnValue = RecentHumidityModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get by id request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/humidities/search', methods=['GET'])
def recent_humidity_get_by_search():
	logging.debug("Received request /recent/humidities/search")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'
		logging.debug("Start arg is: "+ str(start))

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()
		logging.debug("End arg is: "+ str(end))

		dataArray = []
		humArray = RecentHumidityModel.get_by_search(start,end)
		for tempModel in humArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get by search request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/humidities/oldest', methods=['GET'])
def recent_humidity_get_oldest():
	logging.debug("Received request /recent/humidities/oldest")
	startTime = time.monotonic()
	try:
		returnValue = RecentHumidityModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get oldest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/humidities/newest', methods=['GET'])
def recent_humidity_get_newest():
	logging.debug("Received request /recent/humidities/newest")
	startTime = time.monotonic()
	try:
		returnValue = RecentHumidityModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get newest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/humidities/average', methods=['GET'])
def recent_humidity_get_average():
	logging.debug("Received request /recent/humidities/average")
	startTime = time.monotonic()
	try:
		returnValue = RecentHumidityModel.get_average()
		data = RecentHumidityModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get average request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/humidities/average/range', methods=['GET'])
def recent_humidity_get_average_in_range():
	logging.debug("Received request /recent/humidities/average/range")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'
		logging.debug("Start arg is: "+ str(start))

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()
		logging.debug("End arg is: "+ str(end))

		returnValue = RecentHumidityModel.get_average_by_range(start,end)
		data = RecentHumidityModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidity get average in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route("/recent/humidities/reset", methods=["DELETE"])
def recent_humidities_reset():
	logging.debug("Received request /recent/humidities/reset")
	startTime = time.monotonic()
	try:
		# Requires a simple pw
		pw = req.args.get("pw")
		logging.debug("pw arg is: "+ str(pw))
		if pw != "A7G2V9":
			abort(403)
		
		RecentHumidityModel.delete_all()
		elapsedTime = time.monotonic() - startTime
		logging.debug("humidities reset request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/humidities/reset/range', methods=['DELETE'])
def recent_humidities_reset_in_range():
	logging.debug("Received request /recent/humidities/reset/range")
	startTime = time.monotonic()
	try:
		# Requires a simple pw
		pw = req.args.get("pw")
		logging.debug("pw arg is: "+ str(pw))
		if pw != "A7G2V9":
			abort(403)

		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'
		logging.debug("Start arg is: "+ str(start))

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()
		logging.debug("End arg is: "+ str(end))

		RecentHumidityModel.delete_by_range(start,end)
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature reset in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))