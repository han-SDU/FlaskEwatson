import logging
from model.connectionService import ConnectionService

logging.getLogger(__name__)


class TemperatureModel():
    def __init__(self, id, time, value):
        self.id = id
        self.time = time
        self.value = value

    def post(self):
        # Init
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting insert query')
        cur.execute(
            'Insert into tbl_temperature(fld_time,fld_value) values (NOW(),?)', (self.value,))

        logging.debug('Commiting insert changes')
        conn.commit()

        # Update this Object with
        self.id = cur.lastrowid
        self.time = TemperatureModel.get_by_id(self.id).time
        logging.debug('Insert created row with id: ' + str(self.id))

        # Clean and return
        logging.debug('Closing connection')
        conn.close()

        return self.id

    def to_json(self):
        logging.debug('Formatting TemperatureModel to JSON')
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
        logging.debug('Formatting TemperatureModel to average JSON')
        json = {
            'type': 'Temperature average',
            'attributes': {
                    'average': str(avgDecimal),
                    'readingUnit': 'celsius'
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
    def delete_by_range(start, end):
        # Init
        returnValue = True
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting delete query')
        cur.execute(
            'Delete from tbl_temperature where fld_time>=? and fld_time<=?', (start, end,))

        logging.debug('Commiting delete changes')
        conn.commit()

        # Clean and return
        logging.debug('Closing connection')
        conn.close()

        return returnValue

    @staticmethod
    def get_by_id(id):
        # Init
        returnValue = None
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting select query')
        cur.execute('Select * from tbl_temperature where fld_pk_id=?', (id,))

        # Formatting of return data
        logging.debug('Starting formatting to objects')
        for id, time, value in cur:
            returnValue = TemperatureModel(id, time, value)

        # Clean and return
            logging.debug('Closing connection')
        conn.close()

        return returnValue

    @staticmethod
    def get_all():
        # Init
        returnValue = []
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting select query')
        cur.execute('Select * from tbl_temperature')

        # Formatting of return data
        logging.debug('Starting formatting to objects')
        for id, time, value in cur:
            temp = TemperatureModel(id, time, value)
            returnValue.append(temp)

        # Clean and return
            logging.debug('Closing connection')
        conn.close()

        return returnValue

    @staticmethod
    def get_by_search(start, end):
        # Init
        returnValue = []
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting select query')
        cur.execute(
            'Select * from tbl_temperature where fld_time>=? and fld_time<=?', (start, end,))

        # Formatting of return data
        logging.debug('Starting formatting to objects')
        for id, time, value in cur:
            temp = TemperatureModel(id, time, value)
            returnValue.append(temp)

        # Clean and return
            logging.debug('Closing connection')
        conn.close()

        return returnValue

    @staticmethod
    def get_oldest():
        # Init
        returnValue = None
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting select query')
        cur.execute(
            'Select * from tbl_temperature order by fld_time asc limit 1')

        # Formatting of return data
        logging.debug('Starting formatting to objects')
        for id, time, value in cur:
            returnValue = TemperatureModel(id, time, value)

        # Clean and return
            logging.debug('Closing connection')
        conn.close()

        return returnValue

    @staticmethod
    def get_newest():
        # Init
        returnValue = None
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting select query')
        cur.execute(
            'Select * from tbl_temperature order by fld_time desc limit 1')

        # Formatting of return data
        logging.debug('Starting formatting to objects')
        for id, time, value in cur:
            returnValue = TemperatureModel(id, time, value)

        # Clean and return
            logging.debug('Closing connection')
        conn.close()

        return returnValue

    @staticmethod
    def get_average():
        # Init
        returnValue = None
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting select query')
        cur.execute('Select AVG(fld_value) from tbl_temperature')

        # Formatting of return data
        logging.debug('Starting formatting to objects')
        for c in cur:
            returnValue = c[0]  # Average

        # Clean and return
            logging.debug('Closing connection')
        conn.close()

        return returnValue

    @staticmethod
    def get_average_by_range(start, end):
        # Init
        returnValue = None
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug('Starting select query')
        cur.execute(
            'Select AVG(fld_value) from tbl_temperature where fld_time>=? and fld_time<=?', (start, end,))

        # Formatting of return data
        logging.debug('Starting formatting to objects')
        for c in cur:
            returnValue = c[0]  # Average

        # Clean and return
            logging.debug('Closing connection')
        conn.close()

        return returnValue
