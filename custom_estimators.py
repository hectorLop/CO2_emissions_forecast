from abc import ABC, abstractmethod
from sklearn.base import BaseEstimator
import pandas
import numpy
from statsmodels.tsa.statespace.sarimax import SARIMAX

class TimeSeriesEstimator(BaseEstimator, ABC):
    """
    This abstract class defines the common interface for custom time series estimators
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Abstract constructor with custom keyword parameters.
        """
        pass
    
    @abstractmethod
    def fit(self, **kwargs) -> self:
        """
        Fit abstract method to be implemented with custom keyword parameters
        in each estimator.
        """
        pass

    @abstractmethod
    def predict(self, **kwargs) -> list:
        """
        Predict abstract method to be implemented with custom keyword parameters
        in each estimator.
        """
        pass

    def score(self, real_values: numpy.ndarray, predictions: numpy.ndarray) -> float:
        """
        Return the mean absolute error (MAE) on the given data and the predictions.

        Parameters
        ----------
        real_values : array-like of shape (n_samples, 1)
            Real samples of the series
        
        predictions : array-like of shape (n_samples, 1)
            Forecasted values of the series
        
        Returns
        -------
        score : float
            Mean absolute error of real values and predicted ones
        """
        from sklearn.metrics import mean_absolute_error
        return mean_absolute_error(real_values, predictions)

class ARIMAEstimator(TimeSeriesEstimator):
    """
    This class wraps an SARIMAX model into an Estimator

    Parameters
    ----------
    order : iterable or iterable of iterable, optional
        The (p,d,q) order of the model for the number of AR parameters,
        differences, and MA parameters. `d` must be an integer
        indicating the integration order of the process, while
        `p` and `q` may either be an integers indicating the AR and MA
        orders (so that all lags up to those orders are included) or else
        iterables giving specific AR and / or MA lags to include. Default is
        an AR(1) model: (1,0,0).
    seasonal_order : iterable, optional
        The (P,D,Q,s) order of the seasonal component of the model for the
        AR parameters, differences, MA parameters, and periodicity.
        `d` must be an integer indicating the integration order of the process,
        while `p` and `q` may either be an integers indicating the AR and MA
        orders (so that all lags up to those orders are included) or else
        iterables giving specific AR and / or MA lags to include. `s` is an
        integer giving the periodicity (number of periods in season), often it
        is 4 for quarterly data or 12 for monthly data. Default is no seasonal
        effect. Default is (0,0,0,0)
    enforce_stationary : bool, optional
        Whether or not to transform the AR parameters to enforce stationarity
        in the autoregressive component of the model. Default is False.
    enforce_invertibility : bool, optional
        Whether or not to transform the MA parameters to enforce invertibility
        in the moving average component of the model. Default is False.

    Attributes
    ----------
    model : SARIMAX
        SARIMAX object containing the model. Initialized as None.
    model_results:  SARIMAXResults
        SARIMAXResults object containing the results from fitting the 
        SARIMAX model.
    order: Tuple
        Tuple containing the AR parameters, differences and MA parameters.
    seasonal_order: Tuple
        Tuple containing the seasonal component of the model.
    enforce_stationarity : bool
        Whether or not to transform the AR parameters
        to enforce stationarity in the autoregressive
        component of the model.
    enforce_invertibility : bool
        Whether or not to transform the MA parameters
        to enforce invertibility in the moving average
        component of the model.

    Notes
    -----
    This class extends TimeSeriesEstimator in order to be able to be used
    in sklearn Pipelines and GridSearchCV
    """

    def __init__(self, order=(1, 0, 0), seasonal_order=(0, 0, 0, 0),
                 enforce_stationary=False, enforce_invertibility=False):

        self._model = None
        self._model_results = None

        self._order = order
        self._seasonal_order = seasonal_order
        self._enforce_stationary = enforce_stationary
        self._enforce_invertibility = enforce_invertibility


    def fit(self, data: numpy.ndarray) -> self._model_results:
        """
        Fits the given data to the model.
        """
        pass

    def predict(self):
        pass

class ProphetEstimator(TimeSeriesEstimator):
    """
    This class wraps a Prophet model into an Estimator
    """

    def __init__(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass