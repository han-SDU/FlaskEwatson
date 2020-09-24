from model.connectionService import ConnectionService
import logging

logging.getLogger(__name__)

class PressureModel():
	def __init__(self,id,time,value):
		self.id = id
		self.time = time
		self.value = value

	def post(self):
		# Init
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting insert")
		cur.execute('Insert into tbl_pressure(fld_time,fld_value) values (UTC_TIMESTAMP(),?)',(self.value,))

		logging.debug("Committing changes")
		conn.commit()

		# Update this Object with
		self.id = cur.lastrowid
		self.time = PressureModel.get_by_id(self.id).time
		logging.debug("Generated item has id: "+ str(self.id))

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return self.id

	def to_json(self):
		data = {
			'type': 'Pressure sensor reading',
			'id': self.id,
			'attributes': {
				'value': str(self.value),
				'readingTimeUTC': self.time,
				'readingUnit': 'hPa'
				}
			}
		return data

	@staticmethod
	def average_json(avgDecimal):
		json = {
			'type': 'Pressure average',
			'attributes': {
					'average': str(avgDecimal),
					'readingUnit' : 'hPa'
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
		logging.debug("Starting delete")
		cur.execute("Delete from tbl_pressure")

		logging.debug("Committing changes")
		conn.commit()

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return returnValue

	@staticmethod
	def delete_by_range(start,end):
		# Init
		returnValue = True
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting delete")
		cur.execute('Delete from tbl_pressure where fld_time>=? and fld_time<=?', (start,end,))

		logging.debug("Committing changes")
		conn.commit()

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return returnValue

	@staticmethod
	def get_by_id(id):
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting select")
		cur.execute('Select * from tbl_pressure where fld_pk_id=?', (id,))

		# Formatting of return data
		logging.debug("Formatting query data to objects")
		for id,time,value in cur:
			returnValue = PressureModel(id,time,value)

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return returnValue

	@staticmethod
	def get_all():
		# Init
		returnValue = []
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting select")
		cur.execute('Select * from tbl_pressure')

		# Formatting of return data
		logging.debug("Formatting query data to objects")
		for id,time,value in cur:
			temp = PressureModel(id,time,value)
			returnValue.append(temp)

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return returnValue


	@staticmethod
	def get_by_search(start,end):
		# Init
		returnValue = []
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting select")
		cur.execute('Select * from tbl_pressure where fld_time>=? and fld_time<=?', (start,end,))

		# Formatting of return data
		logging.debug("Formatting query data to objects")
		for id,time,value in cur:
			temp = PressureModel(id,time,value)
			returnValue.append(temp)

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return returnValue


	@staticmethod
	def get_oldest():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting select")
		cur.execute('Select * from tbl_pressure order by fld_time asc limit 1')

		# Formatting of return data
		logging.debug("Formatting query data to objects")
		for id,time,value in cur:
			returnValue = PressureModel(id,time,value)

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return returnValue

	@staticmethod
	def get_newest():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting select")
		cur.execute('Select * from tbl_pressure order by fld_time desc limit 1')

		# Formatting of return data
		logging.debug("Formatting query data to objects")
		for id,time,value in cur:
			returnValue = PressureModel(id,time,value)

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return returnValue

	@staticmethod
	def get_average():
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting select")
		cur.execute('Select AVG(fld_value) from tbl_pressure')

		# Formatting of return data
		logging.debug("Formatting query data to objects")
		for c in cur:
			returnValue = c[0] #Average

		# Clean and return
		logging.debug("Closing connection")
		conn.close()

		return returnValue


	@staticmethod
	def get_average_by_range(start,end):
		# Init
		returnValue = None
		conn = ConnectionService.get_connection()
		cur = conn.cursor()

		# Execution
		logging.debug("Starting select")
		cur.execute('Select AVG(fld_value) from tbl_pressure where fld_time>=? and fld_time<=?', (start,end,))

		# Formatting of return data
		logging.debug("Formatting query data to objects")
		for c in cur:
			returnValue = c[0] #Average

		# Clean and return
		logging.debug("Closing connection")
		conn.close()
		
		return returnValue
