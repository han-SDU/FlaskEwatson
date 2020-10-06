# Endpoint for co2 route
from __main__ import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.historic.HistoricCO2Model import HistoricCO2Model
import logging
import time
import mariadb

logging.getLogger(__name__)

@app.route('/historic/co2', methods=['GET'])
def historic_co2_get_all():
	logging.debug("Received request /historic/co2")
	startTime = time.monotonic()
	try:
		dataArray = []
		co2Array = HistoricCO2Model.get_all()
		for tempModel in co2Array:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("co2 get all request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/co2/<int:id>', methods=['GET'])
def historic_co2_get_by_id(id):
	logging.debug("Received request /historic/co2/<id>")
	startTime = time.monotonic()
	try:
		returnValue = HistoricCO2Model.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("co2 get by id request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/co2/search', methods=['GET'])
def historic_co2_get_by_search():
	logging.debug("Received request /historic/co2/search")
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
		co2Array = HistoricCO2Model.get_by_search(start,end)
		for tempModel in co2Array:
			dataArray.append(tempModel.to_json())
		elapsedTime = time.monotonic() - startTime
		logging.debug("co2 get by search request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=dataArray, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/co2/oldest', methods=['GET'])
def historic_co2_get_oldest():
	logging.debug("Received request /historic/co2/oldest")
	startTime = time.monotonic()
	try:
		returnValue = HistoricCO2Model.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("co2 get oldest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/co2/newest', methods=['GET'])
def historic_co2_get_newest():
	logging.debug("Received request /historic/co2/newest")
	startTime = time.monotonic()
	try:
		returnValue = HistoricCO2Model.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		elapsedTime = time.monotonic() - startTime
		logging.debug("co2 get newest request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/co2/average', methods=['GET'])
def historic_co2_get_average():
	logging.debug("Received request /historic/co2/average")
	startTime = time.monotonic()
	try:
		returnValue = HistoricCO2Model.get_average()
		data = HistoricCO2Model.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("co get average request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/co2/average/range', methods=['GET'])
def historic_co2_get_average_in_range():
	logging.debug("Received request /historic/co2/average/range")
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

		returnValue = HistoricCO2Model.get_average_by_range(start,end)
		data = HistoricCO2Model.average_json(returnValue)
		elapsedTime = time.monotonic() - startTime
		logging.debug("co2 get average by range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(200, data=data, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route("/historic/co2/reset", methods=["DELETE"])
def historic_co2_reset():
	logging.debug("Received request /historic/co2/reset")
	startTime = time.monotonic()
	try:
		# Requires a simple pw
		pw = req.args.get("pw")
		logging.debug("pw arg is: "+ str(pw))
		if pw != "A7G2V9":
			abort(403)
		
		HistoricCO2Model.delete_all()
		elapsedTime = time.monotonic() - startTime
		logging.debug("co2 reset request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/historic/co2/reset/range', methods=['DELETE'])
def historic_co2_reset_in_range():
	logging.debug("Received request /historic/co2/reset/range")
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

		HistoricCO2Model.delete_by_range(start,end)
		elapsedTime = time.monotonic() - startTime
		logging.debug("co2 reset in range request time: " + str(round(elapsedTime,5))+ " seconds")
		return res(204, timeUTC=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))