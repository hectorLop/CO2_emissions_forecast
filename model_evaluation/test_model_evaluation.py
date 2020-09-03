import pytest
import numpy

from tests_fixtures.fixtures import supply_df
from models.custom_estimators import ARIMAEstimator
from model_evaluation.model_evaluation import ModelEvaluation
from model_selector.model_selector import ModelSelector

def test_model_evaluation(mocker, supply_df):
    """
    ModelEvaluation Unit test

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing data to test the models
    """
    model = ARIMAEstimator()

    # Mocks model fit method
    mocker.patch.object(model, 'fit')
    # Mocks model predict method to return a numpy array with random values
    mocker.patch.object(model, 'predict', return_value=numpy.random.rand(48))

    model_evaluation = ModelEvaluation(supply_df, model)

    metrics = model_evaluation.cross_validation()

    assert metrics['MAE']
    assert metrics['RMSE']
    assert metrics['MAPE']
    assert metrics['fit_time']