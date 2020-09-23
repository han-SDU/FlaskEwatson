import logging
from model.connectionService import ConnectionService

logging.getLogger(__name__)

class HistoricCO2Model():
    def __init__(self, id, time, value):
        self.id = id
        self.time = time
        self.value = value

    def to_json(self):
        data = {
            'type': 'Historic CO2 sensor reading',
            'id': self.id,
            'attributes': {
                    'value': str(self.value),
                    'readingTimeUTC': self.time,
                'readingUnit': 'ppm'
            }
        }
        return data

    @staticmethod
    def average_json(avgDecimal):
        json = {
            'type': 'Historic CO2 average',
            'attributes': {
                    'average': str(avgDecimal),
                    'readingUnit': 'ppm'
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
        cur.execute("Delete from tbl_historic_co2")

        logging.debug("Committing changes")
        conn.commit()

        # Clean and return
        logging.debug("Closing connection")
        conn.close()

        return returnValue

    @staticmethod
    def delete_by_range(start, end):
        # Init
        returnValue = True
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug("Starting delete")
        cur.execute(
            'Delete from tbl_historic_co2 where fld_time>=? and fld_time<=?', (start, end,))

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
        cur.execute('Select * from tbl_historic_co2 where fld_pk_id=?', (id,))

        # Formatting of return data
        logging.debug("Formatting query data to objects")
        for id, time, value in cur:
            returnValue = HistoricCO2Model(id, time, value)

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
        cur.execute('Select * from tbl_historic_co2')

        # Formatting of return data
        logging.debug("Formatting query data to objects")
        for id, time, value in cur:
            temp = HistoricCO2Model(id, time, value)
            returnValue.append(temp)

        # Clean and return
        logging.debug("Closing connection")
        conn.close()

        return returnValue

    @staticmethod
    def get_by_search(start, end):
        # Init
        returnValue = []
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug("Starting select")
        cur.execute(
            'Select * from tbl_historic_co2 where fld_time>=? and fld_time<=?', (start, end,))

        # Formatting of return data
        logging.debug("Formatting query data to objects")
        for id, time, value in cur:
            temp = HistoricCO2Model(id, time, value)
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
        cur.execute('Select * from tbl_historic_co2 order by fld_time asc limit 1')

        # Formatting of return data
        logging.debug("Formatting query data to objects")
        for id, time, value in cur:
            returnValue = HistoricCO2Model(id, time, value)

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
        cur.execute('Select * from tbl_historic_co2 order by fld_time desc limit 1')

        # Formatting of return data
        logging.debug("Formatting query data to objects")
        for id, time, value in cur:
            returnValue = HistoricCO2Model(id, time, value)

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
        cur.execute('Select AVG(fld_value) from tbl_historic_co2')

        # Formatting of return data
        logging.debug("Formatting query data to objects")
        for c in cur:
            returnValue = c[0]  # Average

        # Clean and return
        logging.debug("Closing connection")
        conn.close()

        return returnValue

    @staticmethod
    def get_average_by_range(start, end):
        # Init
        returnValue = None
        conn = ConnectionService.get_connection()
        cur = conn.cursor()

        # Execution
        logging.debug("Starting select")
        cur.execute(
            'Select AVG(fld_value) from tbl_historic_co2 where fld_time>=? and fld_time<=?', (start, end,))

        # Formatting of return data
        logging.debug("Formatting query data to objects")
        for c in cur:
            returnValue = c[0]  # Average

        # Clean and return
        logging.debug("Closing connection")
        conn.close()

        return returnValue
