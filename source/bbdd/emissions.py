from typing import Tuple, List

class EmissionsManager():
    """
    This class is responsible of the emissions CRUD operations

    Parameters
    ----------
    connector : object
        Object that handles the connection with a database
    
    Attributes
    ----------
    _connector : object
        Object that handles the connection with a database
    """

    def __init__(self, connector: object) -> None:
        self._connector = connector

    def insert_data(self, table_name: str, values: List[Tuple]) -> None:
        """
        Inserts data from a dictionary into a table

        Parameters
        ----------
        name : str
            Table name

        values : List[Tuple]
            List containing a tuple for each observation
        """
        # Creates an argument string to speed up the insert
        argument_string = ",".join(f'({time}, ({hour}), {value})' for (time, hour, value) in values)
        query = f'INSERT INTO {table_name} VALUES ' + argument_string + ' ON CONFLICT DO NOTHING;'
        
        with self._connector.cursor() as cursor:
            cursor.execute(query, values)
        
            self._connector.commit()
            cursor.close()

    def get_last_row(self) -> Tuple[str]:
        query = 'SELECT date FROM emissions ORDER BY date DESC LIMIT 1;'

        with self._connector.cursor() as cursor:
            cursor.execute(query, None)

            # We only got one row
            data = cursor.fetchone()

            cursor.close()

        return data