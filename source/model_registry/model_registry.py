from configparser import ConfigParser
import os
import boto3
import joblib
from io import BytesIO
from datetime import datetime
import json
import pandas

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

    def _dump_model(self, model: object) -> BytesIO:
        """
        Dump a model into a in-memory buffer

        Parameters
        ----------
        model : object
            Trained model

        Returns
        -------
        buffer : BytesIO
            In-memory buffer containing the model data
        """
        with BytesIO() as buffer:
            # Dump the model into a buffer
            joblib.dump(model, buffer)
            # Sets the buffer stream at the start
            buffer.seek(0)

        return buffer

    def _upload_to_aws(self, aws_config: dict, model_data: BytesIO, remote_path : str) -> None:
        """
        Upload a file to a s3 bucket

        Parameters
        ----------
        aws_config : dict
            Dictionary containing aws s3 bucket settings

        model_data : BytesIO
            In-memory buffer containing the model data

        remote_path : str
            Destination file

        Returns
        -------
        uploaded : bool
            True if the file is uploaded succesfully
        """
        # Creates a client with the custom keys
        s3 = boto3.client('s3', aws_access_key_id=aws_config['access_key'],
                        aws_secret_access_key=aws_config['secret_access_key'])

        try:
            # Upload the model to a S3 bucket
            s3.upload_fileobj(Bucket=aws_config['bucket'], Key=remote_path, Fileobj=model_data)
        except FileNotFoundError:
            raise FileNotFoundError("The file was not found")

    def _save_to_remote(self, model: object, aws_config: dict, remote_path: str) -> None:
        """
        Saves a model into a remote repository

        Parameters
        ----------
        model : object
            Trained model

        aws_config : dict
            Dictionary containing aws s3 bucket settings

        remote_path : str
            Destination file in the remote repository
        """
        model_data = self._dump_model(model)
        self._upload_to_aws(aws_config, model_data, remote_path)

    def _create_unique_model_name(self, name: str) -> str:
        """
        Creates a unique model name

        The format is: Model_name-YYY-MM-DD.joblib
        e.g. ARIMA-2020-08-18.joblib

        Parameters
        ----------
        name : str
            Model's name

        Returns
        -------
        unique_model_name : str
            Model's name plus the date of today and the .joblib extension
        """
        date_of_today_str = datetime.today().strftime('%Y-%m-%d')

        return name + '-' + date_of_today_str + ".joblib"

    def publish_model(self, model: object, metrics: dict, training_time: float) -> None:
        """
        Publish a model into a remote repository

        Parameters
        ----------
        model : object
            Trained model

        metrics : dict
            Dictionary containing the model metrics

        training_time : float
            Time necessary to train the model
        """   
        # Gets the model information
        model_info = model.get_info()
        parameters = json.dumps(model_info['parameters'])
        dataset_range_dates = model_info['dataset_start_end']
        name = self._create_unique_model_name(model_info['name'])
        metrics_str = json.dumps(metrics)

        # Gets the aws s3 bucket settings
        aws_config = self._read_aws_config()
        remote_path = aws_config['remote_path'] + name

        # Save the model in the s3 bucket
        self._save_to_remote(model, aws_config, remote_path)

        # Inserts the model info into the model_registry
        self._insert((name, model_info['name'], parameters, metrics_str, remote_path,
                     training_time, dataset_range_dates))
    
    def get_model(self, name: str) -> str:
        query = """
                SELECT
                    *
                FROM
                    registry
                WHERE
                    name = '{}';
                """.format(name)
        
        return pandas.read_sql_query(query, self._connection)