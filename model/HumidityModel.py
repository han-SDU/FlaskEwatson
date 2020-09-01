from model.connectionService import ConnectionService
import socket

class HumidityModel():
	def __init__(self,id,time,value):
		self.id = id
		self.time = time
		self.value = value

	def post(self):
		# Init
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Insert into tbl_humidity(fld_time,fld_value) values (NOW(),?)',(self.value,))
		conn.commit()

		# Update this Object with
		self.id = cur.lastrowid
		self.time = Humidity.get_by_id(self.id).time

		# Clean and return
		conn.close()
		return self.id

	def put(self):
		# Not needing this implementation
		pass

	def to_json(self):
		data = {
			'type': 'Humidity Sensor reading',
			'id': self.id,
			'attributes': {
				'value': str(self.value),
				'readingTime': self.time,
				'readingUnit': '!!!WHAT UNIT!!!'
				}
			}
		return data

	@staticmethod
	def delete(id):
		# Not needing this implementation
		pass

	@staticmethod
	def get_by_id(id):
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_humidity where fld_pk_id=?', (id,))

		# Formatting of return data
		for id,time,value in cur:
			returnValue = HumidityModel(id,time,value)

		# Clean and return
		conn.close()
		return returnValue

	@staticmethod
	def get_all():
		# Init
		returnValue = []
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_humidity')

		# Formatting of return data
		for id,time,value in cur:
			temp = HumidityModel(id,time,value)
			returnValue.append(temp)

		# Clean and return
		conn.close()
		return returnValue


	@staticmethod
	def get_by_search(start,end):
		# Init
		returnValue = []
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_humidity where fld_time>=? and fld_time<=?', (start,end,))

		# Formatting of return data
		for id,time,value in cur:
			temp = HumidityModel(id,time,value)
			returnValue.append(temp)

		# Clean and return
		conn.close()
		return returnValue
