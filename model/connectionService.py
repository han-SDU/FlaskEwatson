import mariadb

class ConnectionService:
	@staticmethod
	def get_connection():
		conn = mariadb.connect(
		user="root",
		password="1234",
		host="localhost",
		database="db_sensor"
		)
		return conn
