import pytest

from source.model_trainer.model_trainer import ModelTrainer
from source.model_trainer.grid_search import ARIMAGridSearch, ProphetGridSearch
from tests.tests_fixtures.fixtures import supply_df
from source.models.custom_estimators import ARIMAEstimator, ProphetEstimator

def test_model_trainer_arima(mocker, supply_df):
    """
    Test the ModelTrainer on the ARIMA model

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    results = {
        'MAE': 15.2,
        'Model': ARIMAEstimator(),
        'Name': 'ARIMA'
    }

    arima_grid_search = ARIMAGridSearch(range_limit=1)
    model_trainer_arima = ModelTrainer(supply_df, arima_grid_search)

    # Mocks the model grid search method which is already tested
    mocker.patch('model_trainer.model_trainer.ARIMAGridSearch.grid_search', return_value=results)
    arima_results = model_trainer_arima.grid_search()

    assert isinstance(arima_results, dict)
    assert arima_results['MAE'] == 15.2
    assert isinstance(arima_results['MAE'], float)
    assert isinstance(arima_results['Model'], ARIMAEstimator)
    assert arima_results['Name'] == 'ARIMA'

def test_model_trainer_prophet(mocker, supply_df):
    """
    Test the ModelTrainer on the Prophet model

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    results = {
        'MAE': 15.2,
        'Model': ProphetEstimator(),
        'Name': 'Prophet'
    }

    prophet_grid_search = ProphetGridSearch()
    model_trainer_prophet = ModelTrainer(supply_df, prophet_grid_search)

    # Mocks the model grid search method which is already tested
    mocker.patch('model_trainer.model_trainer.ProphetGridSearch.grid_search', return_value=results)
    prophet_results = model_trainer_prophet.grid_search()

    assert isinstance(prophet_results, dict)
    assert prophet_results
    assert prophet_results['MAE'] == 15.2
    assert isinstance(prophet_results['Model'], ProphetEstimator)
    assert prophet_results['Name'] == 'Prophet'