from abc import ABC, abstractmethod
import psycopg2
from typing import List, Tuple

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
    def insert_data(self, name: str, values: List[Tuple]) -> None:
        """
        Inserts data from a dictionary into a table or a collection

        Parameters
        ----------
        name : str
            Table or collection name

        values : List[Tuple]
            List containing a tuple for each observation
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
    
class TimescaleConnector(Connector):
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