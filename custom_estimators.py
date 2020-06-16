from abc import ABC, abstractmethod
from sklearn.base import BaseEstimator
import pandas
import numpy

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
    This class wraps an ARIMA model into an Estimator
    """

    def __init__(self):
        pass

    def fit(self):
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