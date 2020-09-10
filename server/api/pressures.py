# Endpoint for pressure route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.PressureModel import PressureModel
import logging
import time
import mariadb

logging.getLogger(__name__)

@app.route('/pressures', methods=['GET'])
def pressure_get_all():
	logging.debug("Recived request /pressures")
	startTime = time.monotonic()
	try:
		dataArray = []
		pressArray = PressureModel.get_all()
		for tempModel in pressArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/<int:id>', methods=['GET'])
def pressure_get_by_id(id):
	logging.debug("Recived request /pressures/<id>")
	startTime = time.monotonic()
	try:
		returnValue = PressureModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get by id request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/search', methods=['GET'])
def pressure_get_by_search():
	logging.debug("Recived request /pressures/search")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		dataArray = []
		pressArray = PressureModel.get_by_search(start,end)
		for tempModel in pressArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/oldest', methods=['GET'])
def pressure_get_oldest():
	logging.debug("Recived request /pressures/oldest")
	startTime = time.monotonic()
	try:
		returnValue = PressureModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get oldest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/newest', methods=['GET'])
def pressure_get_newest():
	logging.debug("Recived request /pressures/newest")
	startTime = time.monotonic()
	try:
		returnValue = PressureModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get newest all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/average', methods=['GET'])
def pressures_get_average():
	logging.debug("Recived request /pressures/average")
	startTime = time.monotonic()
	try:
		returnValue = PressureModel.get_average()
		data = PressureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get average request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/average/range', methods=['GET'])
def pressure_get_average_in_range():
	logging.debug("Recived request /pressures/average/range")
	startTime = time.monotonic()
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = PressureModel.get_average_by_range(start,end)
		data = PressureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get average by range all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))
