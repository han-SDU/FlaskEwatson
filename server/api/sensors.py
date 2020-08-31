# Endpoint for sensor route
from __main__ import app, res, req
from datetime import datetime

@app.route('/sensors', methods=['GET'])
def sensors_get_all():
	return res(501, time=datetime.utcnow()) #200 array in res

@app.route('/sensors/<int:id>', methods=['GET'])
def sensors_get_by_id(id):
	#Depends on how data is stored in the database
	print(id)
	return res(501, time=datetime.utcnow()) #200 single obj in res

@app.route('/sensors/search', methods=['GET'])
def sensors_get_by_search():
	#Depends on how the timestamp is stored in the database
	start = req.args.get('start')
	end = req.args.get('end')
	return res(501, time=datetime.utcnow()) # 200 array in res

@app.route('/sensors', methods=['POST'])
def sensors_post():
	#Probably not needed
	return res(501, time=datetime.utcnow()) #201 created obj in res

@app.route('/sensors/<int:id>', methods=['DELETE'])
def sensors_delete_by_id(id):
	#Probably not needed
	return res(501, time=datetime.utcnow()) #200 no response

@app.route('/sensors/<int:id>', methods=['PUT'])
def sensors_put_by_id(id):
	#Probably not needed
	return res(501, time=datetime.utcnow()) #200 changed obj in res


@app.route('/sensors/dummy', methods=['GET'])
def sensors_get_dummy():
	#An example of how the response should be formatted whgen we have a valid object

	data = {
		'type': 'sensorType',
		'id': 'idOfRessource',
		'attributes': 	{
				'reading': 'over 9000',
				'reading unit': 'cows per kwh'
				},
		'links': 	{
				'self': 'http://IP:PORT/sensors/id',
				'next': '',
				'prev': '',
				'first': '',
				'last': ''
				}
		}
	return res(200, data=data ,time=datetime.utcnow())

