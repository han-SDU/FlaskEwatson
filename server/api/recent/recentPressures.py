# Endpoint for pressure route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.recent.RecentPressureModel import RecentPressureModel
import logging
import time
import mariadb

logging.getLogger(__name__)

@app.route('/recent/pressures', methods=['GET'])
def recent_pressure_get_all():
	logging.debug("Received request /recent/pressures")
	startTime = time.monotonic()
	try:
		dataArray = []
		pressArray = RecentPressureModel.get_all()
		for tempModel in pressArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/pressures/<int:id>', methods=['GET'])
def recent_pressure_get_by_id(id):
	logging.debug("Received request /recent/pressures/<id>")
	startTime = time.monotonic()
	try:
		returnValue = RecentPressureModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get by id request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/pressures/search', methods=['GET'])
def recent_pressure_get_by_search():
	logging.debug("Received request /recent/pressures/search")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		dataArray = []
		pressArray = RecentPressureModel.get_by_search(start,end)
		for tempModel in pressArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/pressures/oldest', methods=['GET'])
def recent_pressure_get_oldest():
	logging.debug("Received request /recent/pressures/oldest")
	startTime = time.monotonic()
	try:
		returnValue = RecentPressureModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get oldest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/pressures/newest', methods=['GET'])
def recent_pressure_get_newest():
	logging.debug("Received request /recent/pressures/newest")
	startTime = time.monotonic()
	try:
		returnValue = RecentPressureModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get newest all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/pressures/average', methods=['GET'])
def recent_pressures_get_average():
	logging.debug("Received request /recent/pressures/average")
	startTime = time.monotonic()
	try:
		returnValue = RecentPressureModel.get_average()
		data = RecentPressureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get average request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/recent/pressures/average/range', methods=['GET'])
def pressure_get_average_in_range():
	logging.debug("Received request /recent/pressures/average/range")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = RecentPressureModel.get_average_by_range(start,end)
		data = RecentPressureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get average by range all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))
