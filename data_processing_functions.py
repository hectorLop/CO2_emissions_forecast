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


def retrieve_emisions_data(start_date_str: str, stop_date_str: str) -> None:
    """
    Creates a csv file with emissions data up to a certain date.

    Dates have to be in format: Year-Month-Day

    Parameters:
        start_date_str (str): Start date to gather data
        stop_date_str (str): Date to stop gathering data
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

    global_dataframe.to_csv('energy_generation_data.csv')


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
