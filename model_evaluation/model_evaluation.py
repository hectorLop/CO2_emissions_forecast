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

    def cross_validation(self, folds=10, fold_size=48) -> Tuple[dict, float]:
        """
        Apply Cross Validation with a given number of folds

        Parameters
        ----------
        folds : int
            Number of folds to use. Default is 10, which means 10 days
        
        fold_size : int
            Size of each fold in hours. Default is 48, which means 48 hours

        Returns
        -------
        metrics : dict
            Metrics for each cv split

        fit_time : float
            The time for fitting the estimator for each cv split
        """
        # Converts days to hours
        offset = folds * fold_size

        while offset > fold_size:
            # Get the whole data less the offset
            train_data = self._data.iloc[:-offset]
            # Get the folf_size from the offset 
            test_data = self._data.iloc[-offset:-offset + fold_size]

            # Train the model and get the fit time
            fit_time = self._measure_fit_time(train_data)

            predictions = self._model.predict()


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