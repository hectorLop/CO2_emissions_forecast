from abc import ABC, abstractmethod
import psycopg2
from pymongo import MongoClient

class Connector(ABC):
    """
    Abstract class to implement connection to a database
    """

    @abstractmethod
    def connect(self, config_parsed: dict) -> object:
        """
        Establish connection with a database

        Parameters
        ----------
        config_parsed : dict
            Dictionary containing the parsed configuration file
        """
        pass

    @abstractmethod
    def insert_data(self, name: str, values: dict) -> None:
        """
        Inserts data from a dictionary into a table or a collection

        Parameters
        ----------
        name : str
            Table or collection name

        values : dict
            Dictionary containing values to be inserted
        """
        pass

class PostgresConnector(Connector):
    """
    Connection to a PostgreSQL database
    """

    def __init__(self) -> None:
        self._connection = None

    def connect(self, config_parsed: dict) -> object:
        """
        Establish connection with a postgreSQL database

        Parameters
        ----------
        config_parsed : dict
            Dictionary containing database settings

        Returns
        -------
        connection : object
            Object which encapsulates a database session
        """
        self._connection = psycopg2.connect(user=config_parsed['postgres']['user'],
                                      password=config_parsed['postgres']['password'],
                                      host=config_parsed['postgres']['host'],
                                      port=config_parsed['postgres']['port'],
                                      database=config_parsed['postgres']['database'])
        
        return self._connection

    def insert_data(self, table_name: str, values: dict) -> None:
        """
        Inserts data from a dictionary into a table

        Parameters
        ----------
        name : str
            Table name

        values : dict
            Dictionary containing values to be inserted
        """
        query = f"""
            INSERT INTO {table_name}
            VALUES (?, ?)
        """

        for key in values.keys():
            self._query(query, (key, values[key]))

    def _query(self, query: str, values=None) -> None:
        """
        Makes a query to the database

        Parameters
        ----------
        query : str
            Query as a string

        values : tuple
            Tuple containing the query values. Default is None
        """
        cursor = self._connection.cursor()
        cursor.execute(query, values)
        cursor.close()

class TimescaleConnector(PostgresConnector):
    """
    Connection to a Timescale database.
    """

    def connect(self, config_parsed: dict) -> object:
        """
        Establish connection with a Timescale database

        Parameters
        ----------
        config_parsed : dict
            Dictionary containing database settings

        Returns
        -------
        connection : object
            Object which encapsulates a database session
        """
        connection = psycopg2.connect(user=config_parsed['timescale']['user'],
                                      password=config_parsed['timescale']['password'],
                                      host=config_parsed['timescale']['host'],
                                      port=config_parsed['timescale']['port'],
                                      database=config_parsed['timescale']['database'])
        
        return connection

class MongoConnector(Connector):
    """
    Connection to a MongoDB database
    """

    def __init__(self) -> None:
        pass

    def connect(self, config_parsed: dict) -> object:
        """
        Establish connection with a MongoDB database

        Parameters
        ----------
        config_parsed : dict
            Dictionary containing database settings

        Returns
        -------
        connection : object
            Object which encapsulates a database session
        """
        client = MongoClient(config_parsed['mongo']['host'], int(config_parsed['mongo']['port']))
        # Gets the database from the client
        connection = client.co2Project_hectorLop

        return connection