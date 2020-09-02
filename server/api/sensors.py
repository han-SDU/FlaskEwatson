# Abstract endpoint grouping  sensor readings together
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.SensorModel import SensorModel
import mariadb

@app.route('/sensors', methods=['GET'])
def sensors_get_all():
	try:
		dataArray = []
		sensor = SensorModel.get_all()
		data = sensor.to_json_array()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))


@app.route('/sensors/search', methods=['GET'])
def sensors_get_by_search():
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		sensor = SensorModel.get_by_search(start,end)
		data = sensor.to_json_array()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/sensors/oldest', methods=['GET'])
def sensors_get_oldest():
	try:
		returnValue = SensorModel.get_oldest()
		data = returnValue.to_single_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/sensors/newest', methods=['GET'])
def sensors_get_newest():
	try:
		returnValue = SensorModel.get_newest()
		data = returnValue.to_single_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/sensors/average', methods=['GET'])
def sensors_get_average():
	try:
		returnValue = SensorModel.get_average()
		data = returnValue.to_average_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/sensors/average/range', methods=['GET'])
def sensors_get_average_in_range():
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = SensorModel.get_average_by_range(start,end)
		data = returnValue.to_average_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))


