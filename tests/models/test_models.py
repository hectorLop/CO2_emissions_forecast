import pytest
import pandas
import numpy

from source.models.custom_estimators import ARIMAEstimator, ProphetEstimator
from tests.tests_fixtures.fixtures import supply_df, supply_pipelines

@pytest.fixture
def supply_fitted_arima(supply_df: pandas.DataFrame) -> None:
    """
    Supplies a trained ARIMA model

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing a test dataset
    """
    arima = ARIMAEstimator()

    return arima.fit(supply_df)

@pytest.fixture
def supply_fitted_prophet(supply_df: pandas.DataFrame) -> None:
    """
    Supplies a trained Prophet model

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing a test dataset
    """
    prophet = ProphetEstimator()

    return prophet.fit(supply_df)

def test_fit_arima_estimator(mocker, supply_df: pandas.DataFrame) -> None:
    """
    Tests the ARIMA fit method

    Parameters
    ----------
    mocker : object
        Mocker object

    supply_df : pandas.DataFrame
        DataFrame containing a test dataset
    """
    arima = ARIMAEstimator()
    
    # Mocks the inner fit method of the SARIMAX model
    mocker.patch('models.custom_estimators.SARIMAX.fit')
    arima.fit(supply_df)

    assert arima._model_results is not None

def test_predict_arima_estimator(supply_fitted_arima: ARIMAEstimator) -> None:
    """
    Tests the ARIMA predict method

    Parameters
    ----------
    supply_fitted_arima : ArimaEstimator
        ARIMA trained model
    """
    predictions = supply_fitted_arima.predict(1)

    assert isinstance(predictions.values, numpy.ndarray)
    assert predictions.values
    assert isinstance(predictions.values[0], float)

def test_arima_get_info(supply_fitted_arima: ARIMAEstimator) -> None:
    """
    Test if the information returned by the model is correct

    Parameters
    ----------
    supply_fitted_arima : ARIMAEstimator
        ARIMA trained model 
    """
    info = supply_fitted_arima.get_info()

    assert isinstance(info, dict)
    assert info['name'] == 'SARIMA'
    assert info['dataset_start_end']
    assert isinstance(info['parameters']['non_seasonal_params'], tuple)
    assert isinstance(info['parameters']['seasonal_params'], tuple)

def test_fit_prophet_estimator(mocker, supply_df: pandas.DataFrame, supply_fitted_prophet: ProphetEstimator) -> None:
    """
    Test the Prophet fit method

    Parameters
    ----------
    supply_df : pandas.DataFrame
        DataFrame containing a test dataset

    supply_fitted_prophet : ProphetEstimator
        Prophet trained model
    """
    # Creates the Prophet estimator
    prophet = ProphetEstimator()
    
    # Mocks the inner fit method of the Prophet model
    mocker.patch('models.custom_estimators.Prophet.fit', return_value=supply_fitted_prophet._model)
    prophet.fit(supply_df)

    # Asserts the params attribute is not empty
    assert prophet._model.params

def test_predict_prophet_estimator(supply_fitted_prophet: ProphetEstimator) -> None:
    """
    Test the Prophet predict method

    Parameters
    ----------
    supply_fitted_prophet : ProphetEstimator
        Prophet trained model
    """
    predictions = supply_fitted_prophet.predict(1)

    assert isinstance(predictions, numpy.ndarray)
    assert predictions
    assert isinstance(predictions[0], float)

def test_prophet_get_info(supply_fitted_prophet: ProphetEstimator):
    """
    Test if the information returned by the model is correct

    Parameters
    ----------
    supply_fitted_prophet : ProphetEstimator
        Prophet trained model
    """ 
    info = supply_fitted_prophet.get_info()

    assert isinstance(info, dict)
    assert info['name'] == 'Prophet'
    assert info['dataset_start_end']
    assert info['parameters']['seasonality_mode']