import pytest
import pandas
from ..grid_search import ARIMAGridSearch, ProphetGridSearch

@pytest.fixture
def supply_df() -> pandas.DataFrame:
    """
    Supply a test dataframe
    """
    # Use this path due to the tests are executed from the main directory
    df = pandas.read_csv('Test_Dataset_2020_01_01_to_2020_02_29.csv')

    # Converts the dates column to datetime object and sets it as the index 
    df['Fecha'] = pandas.to_datetime(df['Fecha'])
    df = df.set_index('Fecha')

    # Sets the dataset frequency
    df.index.freq = pandas.infer_freq(df.index)

    return df

def test_arima_grid_search(supply_df):
    """
    Test the Grid Search on an ARIMA model

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    # Creates train and test data
    train_data = supply_df[:-48]
    test_data = supply_df[-48:]

    # ARIMA Grid Search with a range of paremeters of 0
    arima_grid_search = ARIMAGridSearch(1)

    results = arima_grid_search.grid_search(train_data, test_data)

    # Check the dictionary elements
    assert isinstance(results['MAE'], float)
    assert isinstance(results['Params'], tuple)
    assert results['Name'] == 'ARIMA'

def test_prophet_grid_search(supply_df):
    """
    Test the Grid Search on an Prophet model

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    # Creates train and test data
    train_data = supply_df[:-48]
    test_data = supply_df[-48:]

    # ARIMA Grid Search with a range of paremeters of 0
    arima_grid_search = ProphetGridSearch()

    results = arima_grid_search.grid_search(train_data, test_data)

    # Check the dictionary elements
    assert isinstance(results['MAE'], float)
    assert isinstance(results['Params'], tuple)
    assert results['Name'] == 'Prophet'