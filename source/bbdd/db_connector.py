from __future__ import annotations
import os
from source.bbdd.connectors import Connector
from configparser import ConfigParser
from typing import List, Tuple

class DBConnector():
    """
    This class creates a connection to a PostgreSQL database

    Parameters
    ----------
    connector : Connector
        Connector object to handle a database connection
    
    Attributes
    ----------
    _connector : Connector
        Connector object to handle a database connection
    
    _parser : ConfigParser
        Configuration file parser
    """

    def __init__(self, connector: Connector) -> None:
        self._connector = connector
        self._parser = ConfigParser()

    def connect_to_db(self, ini_file: str) -> object:
        """
        Opens a connection to a database

        Parameters
        ----------
        ini_file : str
            File containing database settings

        Returns
        -------
        connection : object
            Connection object which handles the connection to the database. It
            encapsulates a database session
        """
        # Creates the .ini file absolute path
        ini_path = os.path.join(os.getcwd(), ini_file)
        # Reads the config file with the database settings
        self._parser.read(ini_path)
        # Initialises a connection using the info inside the config file
        connection = self._connector.connect(self._parser)
        
        return connection

    def insert_data(self, name: str, values: List[Tuple]) -> None:
        """
        Inserts data from a dictionary into a table

        Parameters
        ----------
        name : str
            Table or collection name

        values : List[Tuple]
            List containing a tuple for each observation
        """
        self._connector.insert_data(name, values)