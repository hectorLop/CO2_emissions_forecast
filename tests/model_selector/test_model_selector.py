import pytest

from source.model_selector.model_selector import ModelSelector
from tests.tests_fixtures.fixtures import supply_df
from source.models.custom_estimators import TimeSeriesEstimator, ARIMAEstimator

def test_model_selector_select_best_model(mocker, supply_df):
    """
    Test the ModelSelector class

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    model_selector = ModelSelector(supply_df)

    results = {
        'MAE': 15.2,
        'Model': ARIMAEstimator(),
        'Name': 'ARIMA'
    }

    # Mocks the ModelTrainer grid_search method
    mocker.patch('source.model_selector.model_selector.ModelTrainer.grid_search', return_value=results)
    best_model = model_selector.select_best_model()

    assert best_model is not None
    assert isinstance(best_model, TimeSeriesEstimator)