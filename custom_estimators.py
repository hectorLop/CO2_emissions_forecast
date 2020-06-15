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

    def score(self, real_values: pandas.Series, predictions: pandas.Series) -> float:
        """
        Outputs a metric indicating how fit is a timeseries model
        """
        pass