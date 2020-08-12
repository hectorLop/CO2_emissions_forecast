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

    def __init__(self, ini_file : str) -> None:
        self._ini_path = os.path.join(os.getcwd(), ini_file)
        self._config_file = self._read_config_file()

    def _read_config_file(self) -> ConfigParser:
        """
        Gets the parser of the configuration file

        Returns
        -------
        config : ConfigParser
            Configuration file parser
        """
        config = ConfigParser()
        config.read(self._ini_path)

        return config

    def connect_to_db(self) -> psycopg2.connection:
        """
        Opens a connection to a database

        Returns
        -------
        connection : psycopg2.connection
            Connection object which handles the connection to the database. It
            encapsulates a database session
        """
        connection = psycopg2.connect(user=self._config_file['auth']['user'],
                                      password=self._config_file['auth']['password'],
                                      host=self._config_file['db']['host'],
                                      port=self._config_file['db']['port'],
                                      database=self._config_file['db'['database']])
        
        return connection