import mariadb
import logging

logging.getLogger(__name__)


class ConnectionService:
    @staticmethod
    def get_connection():
        conn = mariadb.connect(
            user="root",
            password="1234",
            host="localhost",
            database="db_sensor"
        )
        logging.debug("Connecting to database")
        return conn
