from ..model_selector import ModelSelector
import pytest
from ...tests_fixtures.fixtures import supply_df
from ...models.custom_estimators import TimeSeriesEstimator

def test_model_selector(supply_df):
    """
    Test the ModelSelector class

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    model_selector = ModelSelector(supply_df)

    best_model = model_selector.select_best_model()

    assert best_model is not None
    assert isinstance(best_model, TimeSeriesEstimator)