from abc import ABC, abstractmethod
import psycopg2
import pymongo

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
        pass

class MongoConnector(Connector):
    """
    Connection to a MongoDB database
    """

    def __init__(self) -> None:
        pass

    def connect(self, config_parsed: dict) -> object:
        pass