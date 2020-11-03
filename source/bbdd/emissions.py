from typing import Tuple, List

class EmissionsManager():
    """
    This class is responsible of the CRUD operations related to CO2 emissions

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

    def insert_emissions(self, values: List[Tuple[str, str, float]], table_name='emissions') -> bool:
        """
        Inserts data from a dictionary into a table

        Parameters
        ----------
        values : List[Tuple[str, str, float]]
            List of tuples. Each tuple is composed of (date, hour, value), being the date
            and the hour of type string and the value of tyoe float.
        table_name : str
            Table to insert the data. Default is 'emissions'.
        """
        # Creates an argument string to speed up the insert
        argument_string = ",".join(f'(\'{time}\', \'{hour}\', {value})' for (time, hour, value) in values)
        query = f'INSERT INTO {table_name} VALUES ' + argument_string + ' ON CONFLICT DO NOTHING;'
        
        with self._connector.cursor() as cursor:
            cursor.execute(query, None)
        
            self._connector.commit()
            cursor.close()

        return True

    def get_last_date_inserted(self, table_name='emissions') -> Tuple[str]:
        """
        Gets the most recent date of the CO2 emissions inserted in the database

        Parameters:
        -----------
        table_name : str
            Table to retrieve the data from. Default is 'emissions'.

        Returns
        -------
        data : Tuple[str, str, float]
            Tuple containing the most recent date as a string.
        """
        query = f'SELECT date FROM {table_name} ORDER BY date DESC LIMIT 1;'

        with self._connector.cursor() as cursor:
            cursor.execute(query, None)

            # We get the row or None if the database is empty
            data = cursor.fetchone()

            cursor.close()

        return data

    def get_emissions_data(self, table_name: str, start_date: str, stop_date: str) -> Tuple[str, str, float]:
        """
        Retrieve the emissions data in-between two given dates.

        Parameters
        ----------
        start_date : str
            Date from which to start extracting emissions data.
        stop_date : str
            Date where to stop data extraction.
        
        Returns
        -------
        data : List[Tuple[str, str, float]]
            List of tuples. Each tuple is composed of (date, hour, value), being the date
            and the hour of type string and the value of tyoe float.
        """
        query = f'SELECT date FROM {table_name} WHERE \'{start_date}\' <= date <= \'{stop_date}\' ORDER BY date DESC;'

        with self._connector.cursor() as cursor:
            cursor.execute(query, None)

            data = cursor.fetchall()

            cursor.close()

        return data