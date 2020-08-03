import pytest
from ..tests_fixtures.fixtures import supply_df
from ..models.custom_estimators import ARIMAEstimator
from .model_evaluation import ModelEvaluation

def test_model_evaluation(supply_df):
    """
    ModelEvaluation Unit test

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    model = ARIMAEstimator()

    model_evaluation = ModelEvaluation(supply_df, model)

    metrics = model_evaluation.cross_validation()

    assert metrics['MAE']
    assert metrics['RMSE']
    assert metrics['MAPE']
    assert metrics['fit_time']

def test_model_evaluation_integration():
    pass