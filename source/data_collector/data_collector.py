from source.bbdd.emissions import EmissionsManager
from source.bbdd.db_connector import DBConnector
from source.bbdd.connectors import TimescaleConnector
from datetime import date, timedelta, datetime
import requests
import json
from typing import Dict, List, Tuple

class DataCollector:
    """
    This class is responsible for obtaining the data and storing it in a database.
    TimescaleDB is the chosen database. 

    Attributes
    ----------
    _db_connector : DBConnector
        DBConnector object that handles the creation of the connection with the database and
        the inserting data
    """

    DB_INFO_PATH = 'source/bbdd/db_info.ini'
    ENDPOINT_URL = 'https://demanda.ree.es/WSvisionaMovilesPeninsulaRest/resources/demandaGeneracionPeninsula?fecha='
    CO2_EMISSIONS_FACTOR = {
        'aut': 0.27,
        'car': 0.95,
        'cc': 0.37,
        'cogenResto': 0.27,
        'gf': 0.7,
        'termRenov': 0.27
    }
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self) -> None:
        # Initializes a DBConnector with a Timescale database
        self._db_connector = DBConnector(TimescaleConnector())
        connection = self._db_connector.connect_to_db(self.DB_INFO_PATH)
        # Creates the emission manager to handle CRUD operations
        self._emissions_manager = EmissionsManager(connection)

    def collect_data(self) -> bool:
        """
        Collects new emissions data.

        Returns
        -------
        collected : bool
            True if it has collected new data succesfully.
        """
        emissions = self._retrieve_last_six_hours()

        return self._emissions_manager.insert_emissions(emissions)

    def collect_outdated_data(self) -> bool:
        """
        Collects outdated emissions data.

        Returns
        -------
        collected : bool
            True if it has collected new data succesfully.
        """
        emissions = self._retrieve_outdated_data()

        return self._emissions_manager.insert_emissions(emissions)

    def _retrieve_last_six_hours(self) -> List[Tuple[str, str, float]]:
        """
        Retrieves data from the last two hours

        Returns
        -------
        emissions : List[Tuple[str, str, float]]
            List of tuples. Each tuple is composed of (date, hour, value), being the date
            and the hour of type string and the value of tyoe float
        """
        # Generates the endpoint from which obtain the data
        today_str = self._generate_today_date()
        endpoint = self.ENDPOINT_URL + today_str
        # Retrieves the data from the endpoint
        energy_data = self._retrieve_energy_data(endpoint)

        # Uses the last 12 elements which are the last 2 hours due to the data
        # is in a 10 minutes time format
        emissions = self._generate_emissions(energy_data[-36:])
        
        return emissions

    def _retrieve_outdated_data(self) -> List[Tuple[str, str, float]]:
        """
        Retrieves the emissions to update the database. It has two cases of use:
        the first when the database contains outdated emissions, therefore it will 
        update the emissions since the most recent date, and the last when the database is empty,
        where it will insert the emissions from January of 2015 until today.

        Returns
        -------
        emissions : List[Tuple[str, str, float]]
            List of tuples. Each tuple is composed of (date, hour, value), being the date
            and the hour of type string and the value of tyoe float
        """
        # Gets the last row to get the last update date
        last_row = self._emissions_manager.get_last_row()

        # Gets both start and end dates
        start_date = self._get_start_date(last_row)
        stop_date = datetime.now().date()
        
        emissions = []

        while start_date <= stop_date:           
            # Generates the endpoint
            start_date_str = start_date.strftime(self.DATE_FORMAT)
            endpoint = self.ENDPOINT_URL + start_date_str
            # Gets the data from that day
            energy_data = self._retrieve_energy_data(endpoint)
            # Compute the emissions and extends it to the list
            emissions.extend(self._generate_emissions(energy_data))

            start_date = start_date + timedelta(days=1)

        return emissions

    def _generate_today_date(self) -> str:
        """
        Generates the endpoint to retrieving today's data

        Returns
        -------
        endpoint : str
            Endpoint to retrieving today's data
        """
        today = date.today()
        today_str = today.strftime(self.DATE_FORMAT)

        return today_str

    def _retrieve_energy_data(self, url: str) -> List[Dict]:
        """
        Retrieve the energy data from the last two hours

        Parameters
        ----------
        url : str
            String containing the endpoint url

        Returns
        -------
        json_data : list 
            List containing a dictionary for each observation
        """
        # Gets the raw data in json format
        page = requests.get(url)
        data = page.text

        # Cleans the data to leave only the json part
        data = data.replace('null({"valoresHorariosGeneracion":', '')
        data = data.replace('});', '')

        json_data = json.loads(data)

        return json_data

    def _generate_emissions(self, json_data: List[Dict]) -> List[Tuple]:
        """
        Generates a new list which contains the emissions for each timestamp.
        The list has the following format e.g :
        [
            ('2020-08-27', '21:00', 1000),
            ('2020-08-27', '21:10', 1200),
            ...
        ]

        Parameters
        ----------
        json_data : List[Dict]
            List of dictionaries. Each dictionary contains the data for one observation

        Returns
        -------
        emissions : List[Tuple]
            List of tuples. Each tuples represents one observation
        """
        # Creates a list of tuples with the format (date, hours, emission_value)
        # Compute_emissions output is stored in a list so that the lists can be added
        emissions = [tuple(observation['ts'].split() + [self._compute_emissions(observation)]) for observation in json_data]
         
        return emissions

    def _compute_emissions(self, observation: dict) -> float:
        """
        Compute the emissions generated in an observation

        Parameters
        ----------
        observation : dict
            Dictionary representing an observation in time. It includes
            the timestamp along with the energy generated by each type of energy

        Returns
        -------
        total_emissions : float
            Total sum of emissions for the observation
        """
        # List of energies which generate CO2 emissions
        polluting_energies = ['aut', 'car', 'cc', 'cogenResto', 'gf', 'termRenov']

        # List with the emissions for each energy
        emissions = [observation[energy] * self.CO2_EMISSIONS_FACTOR[energy] for energy in polluting_energies]
        # Get an unique emissions value
        total_emissions = sum(emissions)

        return total_emissions

    def _get_start_date(self, row: List[Tuple]) -> date:
        """
        Gets the date from a given row of the database

        Parameters
        ----------
        row : List[tuple]
            List containing a tuple for each row

        Returns
        -------
        date : date
            Date value 
        """
        # If row is empty, it means the table is empty
        if row is None:
            date = datetime.strptime('2015-01-01', self.DATE_FORMAT).date()
        else:
            # Obtains the date column from the first row
            date = row[0]

        return date