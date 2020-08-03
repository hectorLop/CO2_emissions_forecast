import pytest
from ..tests_fixtures.fixtures import supply_df
from ..models.custom_estimators import ARIMAEstimator
from .model_evaluation import ModelEvaluation
from ..model_selector.model_selector import ModelSelector

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

def test_model_evaluation_integration(supply_df):
    """
    ModelEvaluation integration test

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    model_selector = ModelSelector(supply_df)

    best_model = model_selector.select_best_model()

    model_evaluation = ModelEvaluation(supply_df, best_model)

    metrics = model_evaluation.cross_validation()

    assert metrics['MAE']
    assert metrics['RMSE']
    assert metrics['MAPE']
    assert metrics['fit_time']