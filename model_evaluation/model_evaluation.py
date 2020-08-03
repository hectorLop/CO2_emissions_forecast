from typing import Callable, Tuple
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
        mae, rmse, mape : Tuple
            Tuple containing different metrics

        Metrics
        -------
        - MAE (Mean Absolute Error)
        - RMSE (Root Mean Squared Error)
        - MAPE (Mean Absolute Percentage Error)
        """
        mae = mean_absolute_error(real_values, predictions)
        rmse = numpy.sqrt(mean_squared_error(real_values, predictions))
        mape = numpy.mean(numpy.abs((real_values - predictions) / real_values)) * 100

        return mae, rmse, mape

    def _measure_fit_time(self, train_data: pandas.DataFrame) -> float:
        """
        Measures the execution time of a given function

        Parameters
        ----------
        train_data : pandas.DataFrame
            Train dataset

        Returns
        -------
        end - start _ float
            Elapsed time
        """
        start = time.time()
        self._model.fit(train_data)
        end = time.time()

        return end - start