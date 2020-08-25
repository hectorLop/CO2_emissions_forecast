from pymongo import MongoClient
from ..bbdd.db_connector import DBConnector
from ..bbdd.connectors import MongoConnector

class DataCollector:
    """
    This class is responsible for obtaining the data and storing it in a database.
    MongoDB is the chosen database. 
    """

    DB_INFO_PATH = 'bbdd/db_info.ini'

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

    def retrieve_last_day(self):
        pass

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