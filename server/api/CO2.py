# Endpoint for co2 route
from server.server import app
from flask_json import json_response as res
from flask import request as req
from flask import abort
from datetime import datetime
from model.CO2Model import CO2Model
import mariadb

@app.route('/co2', methods=['GET'])
def co2_get_all():
	try:
		dataArray = []
		co2Array = CO2Model.get_all()
		for tempModel in co2Array:
			dataArray.append(tempModel.to_json())
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/co2/<int:id>', methods=['GET'])
def co2_get_by_id(id):
	try:
		returnValue = CO2.get_by_id(id)
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/co2/search', methods=['GET'])
def co2_get_by_search():
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		dataArray = []
		co2Array = CO2Model.get_by_search(start,end)
		for tempModel in co2Array:
			dataArray.append(tempModel.to_json())
		return res(200, data=dataArray, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/co2/oldest', methods=['GET'])
def co2_get_oldest():
	try:
		returnValue = CO2Model.get_oldest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/co2/newest', methods=['GET'])
def co2_get_newest():
	try:
		returnValue = CO2Model.get_newest()
		if returnValue is None:
			abort(404)
		data = returnValue.to_json()
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/co2/average', methods=['GET'])
def co2_get_average():
	try:
		returnValue = CO2Model.get_average()
		data = CO2Model.average_json(returnValue)
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/co2/average/range', methods=['GET'])
def co2_get_average_in_range():
	try:
		start = req.args.get('start')
		if start is None:
			start = '2020-01-01T00:00:00'

		end = req.args.get('end')
		if end is None:
			end = datetime.utcnow()

		returnValue = CO2Model.get_average_by_range(start,end)
		data = CO2Model.average_json(returnValue)
		return res(200, data=data, time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))

@app.route('/co2', methods=['POST'])
def co2_post():
        #Probably not needed
        abort(501)

@app.route('/temperatures/<int:id>', methods=['DELETE'])
def co2_delete_by_id(id):
        #Probably not needed
        abort(501)

@app.route('/temperatures/<int:id>', methods=['PUT'])
def co2_put_by_id(id):
	#Probably not needed
	abort(501)

@app.route('/temperatures/dummy', methods=['GET'])
def co2_get_dummy():
        #An example of how the response should be formatted whhen we have a valid objct
	try:
		dummy = CO2Model(123,None,666)
		data = dummy.to_json()
		return res(200, data=data ,time=datetime.utcnow())
	except mariadb.Error as e:
		abort(500, str(e))
