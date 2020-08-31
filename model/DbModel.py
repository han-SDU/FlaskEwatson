import mariadb

class DbModel:
	@staticmethod
	def get_connection():
		conn = mariadb.connect(
			user="root",
			password="1234",
			host="localhost",
			database="db_sensor"
		)
		return conn
