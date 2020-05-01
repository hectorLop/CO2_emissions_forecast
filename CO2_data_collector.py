import pandas
from datetime import datetime, timedelta
import requests
import json

CO2_EMISSIONS_FACTOR = {
    'aut': 0.27,
    'car': 0.95,
    'cc': 0.37,
    'cogenResto': 0.27,
    'gf': 0.7,
    'termRenov': 0.27
}
URL = 'https://demanda.ree.es/WSvisionaMovilesPeninsulaRest/resources/demandaGeneracionPeninsula?fecha='
DATETIME_FORMAT = '%Y-%m-%d'


class CO2DataCollector:
    """
    This class models the Data Collector for this specific problem.
    It is the first step on a ML Pipeline

    Attributes:
        url (str): Endpoint to get data
        emissions_factor (dict): Dictionary with emissions factor for each kind of energy
    """

    def __init__(self):
        self.url = URL
        self.emissions_factor = CO2_EMISSIONS_FACTOR
        self.emissions_df = None

    def collect_data(self, start_date_str: str, stop_date_str: str):
        """
        Collects the emissions data from a given time span

        Parameters:
            start_date_str (str): Time span init
            stop_date_str (str): Time span finish
        """

        energy_generation_df = self.__get_energy_generation_data(start_date_str, stop_date_str)
        self.emissions_df = self.__generate_emissions_dataset(energy_generation_df)

    def __get_energy_generation_data(self, start_date_str: str, stop_date_str: str) -> pandas.DataFrame:
        """
        Creates a dataset with energy generation data

        Parameters:
            start_date_str (str): Date to start gathering data.
            stop_date_str (str): Date to stop gathering data
        Returns:
            Dataframe with energy generation data
        """

        # Create the datetime objects
        stop_datetime = datetime.strptime(stop_date_str, DATETIME_FORMAT)
        current_datetime = datetime.strptime(start_date_str, DATETIME_FORMAT)

        # Checks if the stop date is valid
        if not self.__is_valid_stop_date(stop_datetime):
            raise Exception("La fecha de fin no es valida")

        # Creates an empty dataset
        energy_generation_df = pandas.DataFrame()

        while self.__are_different_dates(current_datetime, stop_datetime):
            # Creates the endpoint with the current date
            current_date_str = current_datetime.strftime(DATETIME_FORMAT)
            endpoint = self.url + current_date_str

            # Retrieves the data, generates a json and builds a Dataframe
            data = self.__retrieve_data_from_url(endpoint)
            json_data = self.__generate_json(data)
            current_date_df = pandas.DataFrame(json_data)

            # Appends new data to the Dataframe
            energy_generation_df = pandas.concat([energy_generation_df, current_date_df])

            # Updates the current date
            current_datetime = current_datetime + timedelta(days=1)

        return energy_generation_df

    def __are_different_dates(self, first_date: datetime, second_date: datetime) -> bool:
        """
        Determine if two dates are different

        Parameters:
            first_date (datetime): Datetime object representing the first date
            second_date (datetime): Datetime object representing the second date
        Returns:
            True if different dates
        """

        return first_date != second_date

    def __is_valid_stop_date(self, date: datetime) -> bool:
        """
        Check if a date is valid. A invalid date the one which is greater than the today's date

        Parameters:
            date (datetime): Date to check
        Return:
            True if valid
        """

        today_date = datetime.now()
        today_date_str = today_date.strftime(DATETIME_FORMAT)
        date_str = date.strftime(DATETIME_FORMAT)

        return today_date_str >= date_str

    def __retrieve_data_from_url(self, url: str) -> str:
        """
        Retrieve all the text from a given url

        Parameters:
            url (str): web page's address as string
        Returns:
            Text contained by the url
        """

        page = requests.get(url)
        page_text = page.text

        return page_text

    def __generate_json(self, data: str) -> dict:
        """
        Apply the necessary cleaning and generates a json

        Parameters:
            data (str): Raw data in plaintext
        Returns:
            Dict in json format
        """

        # Clean the data to leave only the json part
        data = data.replace('null({"valoresHorariosGeneracion":', '')
        data = data.replace('});', '')
        json_data = json.loads(data)

        return json_data

    def set_new_endpoint(self, endpoint: str) -> None:
        """
        Sets a new endpoint from which to obtain the data

        Parameters:
            endpoint (str): New endpoint url
        Return:
            None
        """

        self.url = endpoint

    def __generate_emissions_dataset(self, energy_generation_dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Generates a dataset with the sum of CO2 emissions coming from energy generation

        Parameters:
            - energy_generation_dataset (pandas.Dataframe): Dataset of energy generations
        Returns:
            Dataset with two columns: Fecha (timestamp) and Emisiones (Emissions)
        """

        renovable_energies = ['dem', 'eol', 'hid', 'icb', 'inter', 'nuc', 'sol', 'solFot',
                              'solTer']
        no_renovable_energies = ['aut', 'car', 'cc', 'cogenResto', 'gf', 'termRenov']

        # Drop renovable energies
        energy_generation_dataset = energy_generation_dataset.drop(renovable_energies, axis=1)
        # Compute emissions coming from no renovable energies
        energy_generation_dataset = self.__compute_emissions(energy_generation_dataset)
        # Drop no renovable energies
        energy_generation_dataset = energy_generation_dataset.drop(no_renovable_energies, axis=1)
        # Rename columns
        energy_generation_dataset = energy_generation_dataset.rename(columns={'ts': 'Fecha', 'Emissions': 'Emisiones'})

        return energy_generation_dataset

    def __compute_emissions(self, dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Compute the emissions associated to energy generation

        Parameters:
             dataset (pandas.Dataframe): Dataset of energy generation
        Returns:
            Dataset with the Emissions column added
        """

        # Get the total emissions for each row
        emissions_by_energy = [dataset[key] * self.emissions_factor[key] for key in self.emissions_factor]
        dataset['Emissions'] = sum(emissions_by_energy)

        return dataset

    def generate_csv(self, file_name: str) -> None:
        """
        Generates a csv file of the emissions dataset

        Parameters:
            file_name (str): Name of the file
        Returns:
            None
        """
        if self.emissions_df is not None:
            self.emissions_df.to_csv(file_name)
        else:
            print("No existen datos para generar el fichero")
