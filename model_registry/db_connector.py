from configparser import ConfigParser
import os
import psycopg2

class DBConnector():
    """
    This class creates a connection to a PostgreSQL database

    Parameters
    ----------
    ini_file : str
        Name of the configuration file which contains the database settings
    
    Attributes
    ----------
    _ini_path : str
        Configuration file absolute path
    
    _config_file : ConfigParser
        Configuration file parser
    """

    def __init__(self, ini_file: str) -> None:
        self._ini_path = os.path.join(os.getcwd(), ini_file)
        self._config = ConfigParser()

    def connect_to_db(self) -> psycopg2.connection:
        """
        Opens a connection to a database

        Returns
        -------
        connection : psycopg2.connection
            Connection object which handles the connection to the database. It
            encapsulates a database session
        """
        # Reads the config file with the database settings
        self._config.read(self._ini_path)

        connection = psycopg2.connect(user=self._config['auth']['user'],
                                      password=self._config['auth']['password'],
                                      host=self._config['db']['host'],
                                      port=self._config['db']['port'],
                                      database=self._config['db'['database']])
        
        return connection