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

class PostgresConnector(Connector):
    """
    Connection to a PostgreSQL database
    """

    def __init__(self) -> None:
        pass

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
        connection = psycopg2.connect(user=config_parsed['postgres']['user'],
                                      password=config_parsed['postgres']['password'],
                                      host=config_parsed['postgres']['host'],
                                      port=int(config_parsed['postgres']['port']),
                                      database=config_parsed['postgres'['database']])
        
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
        client = MongoClient(config_parsed['host'], int(config_parsed['port']))
        connection = client.co2Project_hectorLop

        return connection