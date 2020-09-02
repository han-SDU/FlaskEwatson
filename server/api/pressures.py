# Endpoint for pressure route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.PressureModel import PressureModel
import mariadb

@app.route('/pressures', methods=['GET'])
def pressure_get_all():
	try:
		dataArray = []
		pressArray = PressureModel.get_all()
		for tempModel in pressArray:
			dataArray.append(tempModel.to_json())
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/<int:id>', methods=['GET'])
def pressure_get_by_id(id):
	try:
		returnValue = PressureModel.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/search', methods=['GET'])
def pressure_get_by_search():
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
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/oldest', methods=['GET'])
def pressure_get_oldest():
	try:
		returnValue = PressureModel.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/newest', methods=['GET'])
def pressure_get_newest():
	try:
		returnValue = PressureModel.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/average', methods=['GET'])
def pressures_get_average():
	try:
		returnValue = PressureModel.get_average()
		data = PressureModel.average_json(returnValue)
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures/average/range', methods=['GET'])
def pressure_get_average_in_range():
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = PressureModel.get_average_by_range(start,end)
		data = PressureModel.average_json(returnValue)
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/pressures', methods=['POST'])
def pressure_post():
        #Probably not needed
        abort(501)

@app.route('/pressures/<int:id>', methods=['DELETE'])
def pressure_delete_by_id(id):
        #Probably not needed
        abort(501)

@app.route('/pressures/<int:id>', methods=['PUT'])
def pressure_put_by_id(id):
	#Probably not needed
	abort(501)

@app.route('/pressures/dummy', methods=['GET'])
def pressure_get_dummy():
        #An example of how the response should be formatted whhen we have a valid objct
	try:
		dummy = PressureModel(123,None,666)
		data = dummy.to_json()
		return res(200, data=data ,time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))
