import pytest
from ..model_trainer import ModelTrainer
from ..grid_search import ARIMAGridSearch, ProphetGridSearch
from .test_grid_search import supply_df

def test_grid_search_model_trainer(supply_df):
    """
    Test the ModelTrainer on the ARIMA and Prophet models
    """
    # Creation of GridSearch object
    arima_grid_search = ARIMAGridSearch(range_limit=1)
    prophet_grid_search = ProphetGridSearch()

    # Creation of ModelTrainer for ARIMA
    model_trainer_arima = ModelTrainer(supply_df, arima_grid_search)
    arima_results = model_trainer_arima.grid_search()

    # Creation of ModelTrainer for Prophet
    model_trainer_prophet = ModelTrainer(supply_df, prophet_grid_search)
    prophet_results = model_trainer_prophet.grid_search()

    assert isinstance(arima_results['MAE'], float)
    assert isinstance(arima_results['Params'], tuple)
    assert arima_results['Name'] == 'ARIMA'

    assert isinstance(prophet_results['MAE'], float)
    assert isinstance(prophet_results['Params'], tuple)
    assert prophet_results['Name'] == 'Prophet'