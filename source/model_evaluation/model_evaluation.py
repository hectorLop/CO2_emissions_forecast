import pandas
import time
import numpy

from typing import Tuple
from source.models.custom_estimators import TimeSeriesEstimator
from sklearn.metrics import mean_squared_error, mean_absolute_error

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

    def cross_validation(self, folds=10, fold_size=48) -> dict:
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
        """
        # Sum of folds
        offset = folds * fold_size

        metrics = {
            'MAE': [],
            'RMSE': [],
            'MAPE': [],
            'fit_time': []
        }

        while offset >= fold_size:
            train_data, test_data = self._get_train_and_test_data(offset, fold_size)

            # Train the model and get the fit time
            fit_time = self._measure_fit_time(train_data)

            # Predict 48 steps by default
            predictions = self._model.predict()

            # Get some metrics from the predictions
            mae, rmse, mape = self._get_metrics(test_data.values, predictions)

            metrics['MAE'].append(mae)
            metrics['RMSE'].append(rmse)
            metrics['MAPE'].append(mape)
            metrics['fit_time'].append(fit_time)

            offset -= fold_size

        return metrics
    
    def _get_train_and_test_data(self, offset: int, fold_size: int) -> Tuple[pandas.DataFrame, pandas.DataFrame]:
        """
        Split the dataset into train and test sets

        Parameters
        ----------
        offset : int
            Index which separates the train and test sets

        fold_size : int
            Test data size
        
        Returns
        -------
        train_data, test_data : Tuple[pandas.DataFrame, pandas.DataFrame]
            Train and test sets
        """
        # Take the whole data less the offset
        train_data = self._data.iloc[:-offset]

        if offset == fold_size:
            # Last iteration, take data from offset to last element
            test_data = self._data.iloc[-offset:]
        else: 
            # Take data from offset plus fold size
            test_data = self._data.iloc[-offset:-offset + fold_size] 

        return train_data, test_data

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