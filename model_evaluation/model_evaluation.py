from typing import Callable
import pandas
from ..models.custom_estimators import TimeSeriesEstimator
from sklearn.metrics import mean_squared_error
import time
import numpy

class ModelEvaluation():
    """
    This class represents a ModelEvaluator to obtain several
    metrics from a model

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing the whole dataset

    model : TimeSeriesEstimator
        Estimator to fit and make predictions

    Attributes
    ----------
    _data : pandas.DataFrame
        DataFrame containing the whole dataset

    _model : TimeSeriesEstimator
        Estimator to fit and make predictions
    """
    
    def __init__(self, data: pandas.DataFrame, model: TimeSeriesEstimator) -> None:
        self._data = data
        self._model = model

    def cross_validation(self):
        pass

    def _get_metrics(self, real_values: numpy.ndarray, predictions: numpy.ndarray):
        """
        Measures some regression metrics
        """
        pass

    def _measure_elapsed_time(self, function: Callable) -> float:
        """
        Measures the execution time of a given function

        Parameters
        ----------
        function : Callable
            Function to be executed

        Returns
        -------
        end - start _ float
            Elapsed time
        """
        start = time.time()
        function()
        end = time.time()

        return end - start