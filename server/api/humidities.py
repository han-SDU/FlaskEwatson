# Endpoint for humidity sensor route
from __main__ import app, res, req
from datetime import datetime

@app.route('/humidities', methods=['GET'])
def humidities_get_all():
        return res(501, time=datetime.utcnow()) #200 array in res

@app.route('/humidities/<int:id>', methods=['GET'])
def humidities_get_by_id(id):
        #Depends on how data is stored in the database
        return res(501, time=datetime.utcnow()) #200 single obj in res

@app.route('/humidities/search', methods=['GET'])
def humidities_get_by_search():
        #Depends on how the timestamp is stored in the database
        start = req.args.get('start')
        end = req.args.get('end')
        return res(501, time=datetime.utcnow()) # 200 array in res

@app.route('/humidities', methods=['POST'])
def humidities_post():
        #Probably not needed
        return res(501, time=datetime.utcnow()) #201 created obj in res

@app.route('/humidities/<int:id>', methods=['DELETE'])
def humidities_delete_by_id(id):
        #Probably not needed
        return res(501, time=datetime.utcnow()) #200 no response

@app.route('/humidities/<int:id>', methods=['PUT'])
def humidities_put_by_id(id):
        #Probably not needed
        return res(501, time=datetime.utcnow()) #200 changed obj in res


@app.route('/humidities/dummy', methods=['GET'])
def humidities_get_dummy():
        #An example of how the response should be formatted whgen we have a valid objc
        data = {
                'type': 'sensorType',
                'id': 'idOfRessource',
                'attributes':   {
                                'reading': 'over 9000',
                                'reading unit': 'cows per kwh'
                                },
                'links':        {
                                'self': 'http://IP:PORT/sensors/id',
                                'next': '',
                                'prev': '',
                                'first': '',
                                'last': ''
                                }
                }
        return res(200, data=data ,time=datetime.utcnow())


























































































