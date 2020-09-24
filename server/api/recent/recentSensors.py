# Abstract endpoint grouping  sensor readings together
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.recent.RecentSensorModel import RecentSensorModel
import logging
import time
import mariadb

logging.getLogger(__name__)


@app.route('/recent/sensors', methods=['GET'])
def recent_sensors_get_all():
	logging.debug("Received request /recent/sensors")
	startTime = time.monotonic()
	try:
		dataArray = []
		sensor = RecentSensorModel.get_all()
		data = sensor.to_json_array()
		elapsedTime = time.monotonic() - startTime
		logging.debug("sensors get all request time: " +
					  str(round(elapsedTime, 5)) + " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		logging.exception(e)
		abort(500, str(e))


@app.route('/recent/sensors/search', methods=['GET'])
def recent_sensors_get_by_search():
	logging.debug("Received request /recent/sensors/search")
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

		sensor = RecentSensorModel.get_by_search(start, end)
		data = sensor.to_json_array()
		elapsedTime = time.monotonic() - startTime
		logging.debug("sensors get by id request time: " +
					  str(round(elapsedTime, 5)) + " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		logging.exception(e)
		abort(500, str(e))


@app.route('/recent/sensors/oldest', methods=['GET'])
def recent_sensors_get_oldest():
	logging.debug("Received request /recent/sensors/oldest")
	startTime = time.monotonic()
	try:
		returnValue = RecentSensorModel.get_oldest()
		data = returnValue.to_single_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("sensors get oldest request time: " +
					  str(round(elapsedTime, 5)) + " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		logging.exception(e)
		abort(500, str(e))


@app.route('/recent/sensors/newest', methods=['GET'])
def recent_sensors_get_newest():
	logging.debug("Received request /recent/sensors/newest")
	startTime = time.monotonic()
	try:
		returnValue = RecentSensorModel.get_newest()
		data = returnValue.to_single_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("sensor get newest request time: " +
					  str(round(elapsedTime, 5)) + " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		logging.exception(e)
		abort(500, str(e))


@app.route('/recent/sensors/average', methods=['GET'])
def recent_sensors_get_average():
	logging.debug("Received request /recent/sensors/average")
	startTime = time.monotonic()
	try:
		returnValue = RecentSensorModel.get_average()
		data = returnValue.to_average_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("sensors get average all request time: " +
					  str(round(elapsedTime, 5)) + " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		logging.exception(e)
		abort(500, str(e))


@app.route('/recent/sensors/average/range', methods=['GET'])
def sensors_get_average_in_range():
	logging.debug("Received request /recent/sensors/average/range")
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

		sensor = RecentSensorModel.get_average_by_range(start, end)
		data = sensor.to_average_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("sensors get by average range request time: " +
					  str(round(elapsedTime, 5)) + " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		logging.exception(e)
		abort(500, str(e))

@app.route("/recent/sensors/reset", methods=["DELETE"])
def recent_sensors_reset():
	logging.debug("Received request /recent/sensors/reset")
	startTime = time.monotonic()
	try:
		# Requires a simple pw
		pw = req.args.get("pw")
		logging.debug("pw arg is: "+ str(pw))
		if pw != "A7G2V9":
			abort(403)
		
		RecentSensorModel.delete_all()
		elapsedTime = time.monotonic() - startTime
		logging.debug("sensors reset request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		logging.exception(e)
		abort(500, str(e))

@app.route('/recent/sensors/reset/range', methods=['DELETE'])
def recent_sensors_reset_in_range():
	logging.debug("Received request /recent/sensors/reset/range")
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

		RecentSensorModel.delete_by_range(start,end)
		elapsedTime = time.monotonic() - startTime
		logging.debug("sensors reset in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		logging.exception(e)
		abort(500, str(e))