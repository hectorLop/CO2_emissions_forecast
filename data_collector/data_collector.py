from ..bbdd.db_connector import DBConnector
from ..bbdd.connectors import MongoConnector
from datetime import date, datetime, time, timedelta

class DataCollector:
    """
    This class is responsible for obtaining the data and storing it in a database.
    MongoDB is the chosen database. 
    """

    DB_INFO_PATH = 'bbdd/db_info.ini'
    ENDPOINT_URL = 'https://demanda.ree.es/WSvisionaMovilesPeninsulaRest/resources/demandaGeneracionPeninsula?fecha='

    def __init__(self) -> None:
        self._connection = self._create_connection()

    def _create_connection(self) -> object:
        """
        Creates a connection with a database

        Returns
        -------
        connection : object
            Object which handles the connection to the database
        """
        # Initializes a DBConnector with a MongoConnector
        db_connector = DBConnector(MongoConnector())

        return db_connector.connect_to_db(self.DB_INFO_PATH)

    def retrieve_last_day(self) -> None:
        """
        Retrieves data from the previous day
        """
        previous_day_str = self._get_previous_day_date()

    def _get_previous_day_date(self) -> str:
        """
        Gets the previous day date as a string

        Returns
        -------
        previous_day_str : str
            String representing the date of the previous day in the format YYYY-MM-DD
        """
        today = date.today()
        previous_day = today - timedelta(days = 1)

        return previous_day.strftime('%Y-%m-%d')

    def insert_raw_data(self, data: dict) -> None:
        """
        Inserts a new record in the database

        Parameters
        ----------
        data : dict
            Dictionary containing the data to be stored
        """
        # Gets the collection which stores raw data
        collection = self._connection.raw_collector

        collection.insert_one(data)