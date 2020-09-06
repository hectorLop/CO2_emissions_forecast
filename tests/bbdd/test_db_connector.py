import pytest
from source.bbdd.db_connector import DBConnector
from source.bbdd.connectors import PostgresConnector, MongoConnector

def test_postgres_connector():
    """
    Test the DBConnector with the PostgresConnector
    """
    connector = PostgresConnector()
    db_connector = DBConnector(connector)

    connection = db_connector.connect_to_db('source/bbdd/db_info.ini')

    assert connection is not None

def test_mongo_connector():
    """
    Test the DBConnector with the MongoConnector
    """
    connector = MongoConnector()
    db_connector = DBConnector(connector)

    connection = db_connector.connect_to_db('source/bbdd/db_info.ini')

    assert connection is not None