# Endpoint for humidity route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.HumidityModel import HumidityModel
import mariadb

@app.route('/humidities', methods=['GET'])
def humidity_get_all():
	try:
		dataArray = []
		humArray = HumidityModel.get_all()
		for tempModel in humArray:
			dataArray.append(tempModel.to_json())
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/<int:id>', methods=['GET'])
def humidity_get_by_id(id):
	try:
		returnValue = HumidityModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/search', methods=['GET'])
def humidity_get_by_search():
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
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/oldest', methods=['GET'])
def humidity_get_oldest():
	try:
		returnValue = HumidityModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/newest', methods=['GET'])
def humidity_get_newest():
	try:
		returnValue = HumidityModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/average', methods=['GET'])
def humidity_get_average():
	try:
		returnValue = HumidityModel.get_average()
		data = HumidityModel.average_json(returnValue)
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities/average/range', methods=['GET'])
def humidity_get_average_in_range():
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = HumidityModel.get_average_by_range(start,end)
		data = HumidityModel.average_json(returnValue)
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/humidities', methods=['POST'])
def humidity_post():
        #Probably not needed
        abort(501)

@app.route('/humidities/<int:id>', methods=['DELETE'])
def humidity_delete_by_id(id):
        #Probably not needed
        abort(501)

@app.route('/humidities/<int:id>', methods=['PUT'])
def humidity_put_by_id(id):
	#Probably not needed
	abort(501)

@app.route('/humidities/dummy', methods=['GET'])
def humidity_get_dummy():
        #An example of how the response should be formatted whhen we have a valid objct
	try:
		dummy = HumidityModel(123,None,666)
		data = dummy.to_json()
		return res(200, data=data ,time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

