from typing import Callable
import pandas
from ..models.custom_estimators import TimeSeriesEstimator
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_per
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

    def _get_metrics(self, real_values: numpy.ndarray, predictions: numpy.ndarray) -> dict:
        """
        Measures some regression metrics

        Parameters
        ----------
        real_values : numpy.ndarray
            Numpy array containing the real observations

        predictions : numpy.ndarray
            Numpy array containing predictions

        Returns
        -------
        metrics : dictionary
            Dictionary containing several metrics

        Metrics
        -------
        - MAE (Mean Absolute Error)
        - RMSE (Root Mean Squared Error)
        - MAPE (Mean Absolute Percentage Error)
        """
        metrics = {}
        metrics['MAE'] = mean_absolute_error(real_values, predictions)
        metrics['RMSE'] = numpy.sqrt(mean_squared_error(real_values, predictions))
        metrics['MAPE'] = numpy.mean(numpy.abs((real_values - predictions) / real_values)) * 100

        return metrics

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