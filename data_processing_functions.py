from datetime import datetime, timedelta
import requests
import pandas
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


def retrieve_emisions_data(start_date_str: str, stop_date_str: str, file_name: str) -> None:
    """
    Creates a csv file with emissions data up to a certain date.

    Dates have to be in format: Year-Month-Day

    Parameters:
        start_date_str (str): Start date to gather data
        stop_date_str (str): Date to stop gathering data
        file_name (str): Name of csv file
    Returns:
        None
    """

    stop_datetime = datetime.strptime(stop_date_str, DATETIME_FORMAT)
    current_datetime = datetime.strptime(start_date_str, DATETIME_FORMAT)
    global_dataframe = pandas.DataFrame()

    while are_different_dates(current_datetime, stop_datetime):
        # Create URL with the current date
        current_date_str = current_datetime.strftime(DATETIME_FORMAT)
        url = URL + current_date_str

        # Retrieve, process and appends new data
        data = retrieve_data_from_url(url)
        dataframe = process_data(data)
        global_dataframe = pandas.concat([global_dataframe, dataframe])

        # Decrease one day
        current_datetime = current_datetime - timedelta(days=1)

    global_dataframe.to_csv(file_name)


def are_different_dates(first_date: datetime, second_date: datetime) -> bool:
    """
    Determine if two dates are different

    Parameters:
        first_date (datetime): Datetime object representing the first date
        second_date (datetime): Datetime object representing the second date
    Returns:
        True if different
    """

    return first_date != second_date


def retrieve_data_from_url(url: str) -> str:
    """
    Retrieve all the text from a given url

    Parameters:
        url: web page's address as string
    Returns:
        Soup with all the text in the web page
    """

    page = requests.get(url)
    page_text = page.text

    return page_text


def process_data(data: str) -> pandas.DataFrame:
    """
    Apply some preprocessing on data and returns a DataFrame

    Parameters:
        data (str): data in plaintext
    Returns:
        Dataframe with data
    """

    # Clean the data to leave only the json part
    data = data.replace('null({"valoresHorariosGeneracion":', '')
    data = data.replace('});', '')
    data = json.loads(data)

    # Creates the dataframe
    dataframe = pandas.DataFrame(data)

    return dataframe


def generate_emissions_dataset(energy_generation_dataset: pandas.DataFrame) -> pandas.DataFrame:
    """
    Generates a dataset with the sum of CO2 emissions coming from energy generation

    Parameters:
        - energy_generation_dataset (pandas.Dataframe): Dataset of energy generations
    Returns:
        Dataset with two columns: Fecha (timestamp) and Emisiones (Emissions)
    """

    renovable_energies = ['dem', 'eol', 'hid', 'icb', 'inter', 'nuc', 'sol', 'solFot',
                       'solTer', 'Unnamed: 0']
    no_renovable_energies = ['aut', 'car', 'cc', 'cogenResto', 'gf', 'termRenov']

    # Drop renovable energies
    energy_generation_dataset = energy_generation_dataset.drop(renovable_energies, axis=1)
    # Compute emissions coming from no renovable energies
    energy_generation_dataset = compute_emissions(energy_generation_dataset)
    # Drop no renovable energies
    energy_generation_dataset = energy_generation_dataset.drop(no_renovable_energies, axis=1)

    energy_generation_dataset = energy_generation_dataset.rename(columns={'ts': 'Fecha', 'Emissions': 'Emisiones'})

    return energy_generation_dataset


def compute_emissions(dataset: pandas.DataFrame) -> pandas.DataFrame:
    """
    Compute the emissions associated to energy generation

    Parameters:
         dataset (pandas.Dataframe): Dataset of energy generation
    Returns:
        Dataset with the Emissions column added
    """

    dataset['Emissions'] = dataset['aut'] * CO2_EMISSIONS_FACTOR['aut'] + dataset['car'] * CO2_EMISSIONS_FACTOR['car'] \
                       + dataset['cc'] * CO2_EMISSIONS_FACTOR['cc'] + dataset['cogenResto'] * CO2_EMISSIONS_FACTOR['cogenResto'] \
                       + dataset['gf'] * CO2_EMISSIONS_FACTOR['gf'] + dataset['termRenov'] * CO2_EMISSIONS_FACTOR['termRenov']

    return dataset


def reverse_dataset(dataset: pandas.DataFrame) -> pandas.DataFrame:
    """
    Reverse the rows order of a given dataset

    Parameters:
        dataset (pandas.Dataframe): Dataset to be reversed
    Returns:
        Reversed dataset
    """

    return dataset.iloc[::-1]
