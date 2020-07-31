import pytest
import pandas
from ..grid_search import ARIMAGridSearch, ProphetGridSearch
from ...tests_fixtures.fixtures import supply_df
from ...models.custom_estimators import ARIMAEstimator, ProphetEstimator

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
    arima_grid_search = ARIMAGridSearch(range_limit=1)

    results = arima_grid_search.grid_search(train_data, test_data)

    # Check the dictionary elements
    assert isinstance(results['MAE'], float)
    assert isinstance(results['Model'], ARIMAEstimator)
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
    assert isinstance(results['Model'], ProphetEstimator)
    assert results['Name'] == 'Prophet'