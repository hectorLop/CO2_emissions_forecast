from configparser import ConfigParser
from typing import Any, Tuple
from .config_reader import ConfigReader
import json
import os
import boto3
import joblib

class ModelRegistry:
    """
    This class represents a Model Registry to save models and have a log of it

    Parameters
    ----------
    connection : object
        Database session

    table_name : str
        Registry table name. Default is 'registry'

    Attributes
    ----------
    _connection : object
        Database session

    _table_name : str
        Registry table name
    """

    KEYS_FILENAME = 'aws_config.ini'

    def __init__(self, connection: object, table_name='registry') -> None:
        self._connection = connection
        self._table_name = table_name

    def _insert(self, values: tuple) -> None:
        """
        Inserts info to the database

        Parameters
        ----------
        values : tuple
            Tuple containing the values to be inserted
        """
        query = """
                INSERT INTO {}
                (name, model, parameters, metrics, remote_path, training_path, dataset)
                VALUES (?, ?, ?, ?, ?, ?, ?)""".format(self._table_name)
        self._query(query, values)

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
    
    def _save_to_remote(path: str, filename: str, model: object) -> None:
        pass
    
    def _read_aws_config(self) -> dict:
        """
        Gets the access and secret keys
        
        Returns
        -------
        access_key, secret_acces_key : tuple
            Tuple containing both keys as strings
        """
        # Gets the absolute path of the file containing the keys
        ini_path = os.path.join(os.getcwd(), self.KEYS_FILENAME)

        parser = ConfigParser()
        # Reads the config file
        parser.read(ini_path)

        return parser['settings']
    
    def _upload_to_aws(self, local_file: str, bucket: str, remote_path: str) -> bool:
        """
        Upload a file to a s3 bucket

        Parameters
        ----------
        local_file : str
            File to be uploaded

        bucket : str
            Bucket name

        remote_path : str
            Destination file

        Returns
        -------
        uploaded : bool
            True if the file is uploaded succesfully
        """
        aws_config = self._read_aws_config()

        s3 = boto3.client('s3', aws_access_key_id=aws_config['access_key'],
                      aws_secret_access_key=aws_config['secret_access_key'])

        try:
            s3.upload_file(local_file, bucket, s3_file)
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False

    def publish_model(self, model: object, name: str, parameters: tuple, metrics: Any,
                      training_time: float, dataset_range: str) -> None:
        pass

    def get_model_info(self, name: str) -> str:
        pass