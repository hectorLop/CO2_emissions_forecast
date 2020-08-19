from abc import ABC, abstractmethod

class Connector(ABC):
    """
    Abstract class to implement connection to a database
    """

    @abstractmethod
    def connect(self) -> object:
        """
        Establish connection with a database
        """
        pass

class PostgresConnector(Connector):
    """
    Connection to a PostgreSQL database
    """

    def __init__(self) -> None:
        pass

    def connect(self) -> object:
        pass

class MongoConnector(Connector):
    """
    Connection to a MongoDB database
    """

    def __init__(self) -> None:
        pass

    def connect(self) -> object:
        pass