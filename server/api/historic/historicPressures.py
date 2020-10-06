# Endpoint for pressure route
from __main__ import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.historic.HistoricPressureModel import HistoricPressureModel
import logging
import time
import mariadb

logging.getLogger(__name__)

@app.route('/historic/pressures', methods=['GET'])
def historic_pressure_get_all():
	logging.debug("Received request /pressures")
	startTime = time.monotonic()
	try:
		dataArray = []
		pressArray = HistoricPressureModel.get_all()
		for tempModel in pressArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/pressures/<int:id>', methods=['GET'])
def historic_pressure_get_by_id(id):
	logging.debug("Received request /pressures/<id>")
	startTime = time.monotonic()
	try:
		returnValue = HistoricPressureModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get by id request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/pressures/search', methods=['GET'])
def historic_pressure_get_by_search():
	logging.debug("Received request /historic/pressures/search")
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
		pressArray = HistoricPressureModel.get_by_search(start,end)
		for tempModel in pressArray:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("temperature get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/pressures/oldest', methods=['GET'])
def historic_pressure_get_oldest():
	logging.debug("Received request /historic/pressures/oldest")
	startTime = time.monotonic()
	try:
		returnValue = HistoricPressureModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get oldest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/pressures/newest', methods=['GET'])
def historic_pressure_get_newest():
	logging.debug("Received request /historic/pressures/newest")
	startTime = time.monotonic()
	try:
		returnValue = HistoricPressureModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get newest all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/pressures/average', methods=['GET'])
def historic_pressures_get_average():
	logging.debug("Received request /historic/pressures/average")
	startTime = time.monotonic()
	try:
		returnValue = HistoricPressureModel.get_average()
		data = HistoricPressureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get average request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/pressures/average/range', methods=['GET'])
def historic_pressure_get_average_in_range():
	logging.debug("Received request /historic/pressures/average/range")
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

		returnValue = HistoricPressureModel.get_average_by_range(start,end)
		data = HistoricPressureModel.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("pressure get average by range all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route("/historic/pressures/reset", methods=["DELETE"])
def historic_pressures_reset():
	logging.debug("Received request /historic/pressures/reset")
	startTime = time.monotonic()
	try:
		# Requires a simple pw
		pw = req.args.get("pw")
		logging.debug("pw arg is: "+ str(pw))
		if pw != "A7G2V9":
			abort(403)
		
		HistoricPressureModel.delete_all()
		elapsedTime = time.monotonic() - startTime
		logging.debug("Pressure reset request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/pressures/reset/range', methods=['DELETE'])
def historic_pressures_reset_in_range():
	logging.debug("Received request /historic/pressures/reset/range")
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

		HistoricPressureModel.delete_by_range(start,end)
		elapsedTime = time.monotonic() - startTime
		logging.debug("Pressure reset in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))