from model.connectionService import ConnectionService

class TemperatureModel():
	def __init__(self,id,time,value):
		self.id = id
		self.time = time
		self.value = value

	def post(self):
		# Init
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Insert into tbl_temperature(fld_time,fld_value) values (NOW(),?)',(self.value,))
		conn.commit()

		# Update this Object with
		self.id = cur.lastrowid
		self.time = TemperatureModel.get_by_id(self.id).time

		# Clean and return
		conn.close()
		return self.id

	def put(self):
		# Not needing this implementation
		pass

	def to_json(self):
		data = {
			'type': 'Temperature sensor reading',
			'id': self.id,
			'attributes': {
				'value': str(self.value),
				'readingTime': self.time,
				'readingUnit': 'celsius'
				}
			}
		return data

	@staticmethod
	def average_json(avgDecimal):
		json = {
			'type': 'Temperature average',
			'attributes': {
					'average': str(avgDecimal),
					'readingUnit' : 'celsius'
					}
			}
		return json

	@staticmethod
	def delete_all():
		# Init
		returnValue = True
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute("Delete from tbl_temperature")
		conn.commit()

		# Clean and return
		conn.close()
		return returnValue

	@staticmethod
	def delete_by_range(start,end):
		# Init
		returnValue = True
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Delete from tbl_temperature where fld_time>=? and fld_time<=?', (start,end,))
		conn.commit()

		# Clean and return
		conn.close()

	@staticmethod
	def get_by_id(id):
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_temperature where fld_pk_id=?', (id,))

		# Formatting of return data
		for id,time,value in cur:
			returnValue = TemperatureModel(id,time,value)

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
		cur.execute('Select * from tbl_temperature')

		# Formatting of return data
		for id,time,value in cur:
			temp = TemperatureModel(id,time,value)
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
		cur.execute('Select * from tbl_temperature where fld_time>=? and fld_time<=?', (start,end,))

		# Formatting of return data
		for id,time,value in cur:
			temp = TemperatureModel(id,time,value)
			returnValue.append(temp)

		# Clean and return
		conn.close()
		return returnValue

	@staticmethod
	def get_oldest():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_temperature order by fld_time asc limit 1')

		# Formatting of return data
		for id,time,value in cur:
			returnValue = TemperatureModel(id,time,value)

		# Clean and return
		conn.close()
		return returnValue

	@staticmethod
	def get_newest():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select * from tbl_temperature order by fld_time desc limit 1')

		# Formatting of return data
		for id,time,value in cur:
			returnValue = TemperatureModel(id,time,value)

		# Clean and return
		conn.close()
		return returnValue

	@staticmethod
	def get_average():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select AVG(fld_value) from tbl_temperature')

		# Formatting of return data
		for c in cur:
			returnValue = c[0] #Average

		# Clean and return
		conn.close()
		return returnValue


	@staticmethod
	def get_average_by_range(start,end):
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		cur.execute('Select AVG(fld_value) from tbl_temperature where fld_time>=? and fld_time<=?', (start,end,))

		# Formatting of return data
		for c in cur:
			returnValue = c[0] #Average

		# Clean and return
		conn.close()
		return returnValue
