from abc import ABC, abstractmethod
import psycopg2

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
    Handles the connection to a PostgreSQL database
    """

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
                                      port=config_parsed['postgres']['port'],
                                      database=config_parsed['postgres']['database'])
        
        return connection
    
class TimescaleConnector(Connector):
    """
    Handles the connection to a Timescale database.
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