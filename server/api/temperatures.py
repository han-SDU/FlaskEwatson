# Endpoint for temperatures route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.TemperatureModel import TemperatureModel
import mariadb

@app.route('/temperatures', methods=['GET'])
def temperatures_get_all():
	try:
		dataArray = []
		temperatureArray = TemperatureModel.get_all()
		for tempModel in temperatureArray:
			dataArray.append(tempModel.to_json())
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/<int:id>', methods=['GET'])
def temperatures_get_by_id(id):
	try:
		returnValue = TemperatureModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/search', methods=['GET'])
def temperatures_get_by_search():
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
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/oldest', methods=['GET'])
def temperatures_get_oldest():
	try:
		returnValue = TemperatureModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/newest', methods=['GET'])
def temperatures_get_newest():
	try:
		returnValue = TemperatureModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/average', methods=['GET'])
def temperatures_get_average():
	try:
		returnValue = TemperatureModel.get_average()
		data = TemperatureModel.average_json(returnValue)
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/temperatures/average/range', methods=['GET'])
def temperatures_get_average_in_range():
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = TemperatureModel.get_average_by_range(start,end)
		data = TemperatureModel.average_json(returnValue)
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))


@app.route('/temperatures', methods=['POST'])
def temperatures_post():
        #Probably not needed
        abort(501)

@app.route('/temperatures/<int:id>', methods=['DELETE'])
def temperatures_delete_by_id(id):
        #Probably not needed
        abort(501)

@app.route('/temperatures/<int:id>', methods=['PUT'])
def temperatures_put_by_id(id):
	#Probably not needed
	abort(501)

@app.route('/temperatures/dummy', methods=['GET'])
def temperatures_get_dummy():
        #An example of how the response should be formatted whhen we have a valid objct
	try:
		dummy = TemperatureModel(123,None,666)
		data = dummy.to_json()
		return res(200, data=data ,time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))
