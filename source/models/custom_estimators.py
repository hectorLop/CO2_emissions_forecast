from __future__ import annotations
from abc import ABC, abstractmethod
from sklearn.base import BaseEstimator
import pandas
import numpy
from statsmodels.tsa.statespace.sarimax import SARIMAX
from fbprophet import Prophet

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
    def fit(self, **kwargs) -> TimeSeriesEstimator:
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

    @abstractmethod
    def get_info(self) -> dict:
        """
        Returns estimmator significative information such as:
            - Estimator name
            - Parameters
            - Start and end dates from the dataset used to train the estimator
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

    def _get_start_and_end_dates(self, data: pandas.DataFrame) -> str:
        """
        Gets the first and last dates from a DatetimeIndex
        It assumes that the dataset 
        """
        format = '%Y-%m-%d %H:%M'
        start = data.index[0].strftime(format)
        end = data.index[-1].strftime(format)

        return start + ', ' + end

class ARIMAEstimator(TimeSeriesEstimator):
    """
    This class wraps up an SARIMAX model into an Estimator

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

        self._dataset_start_end = ''

    def fit(self, data: numpy.ndarray, y=None) -> ARIMAEstimator:
        """
        Fits the given data to the model.

        Parameters
        ----------
        data : array_like
            The observed time-series
        
        Returns
        -------
        self : ARIMAEstimator
            Self ARIMAEstimator object
        """
        # Gets the start and the end of the dataset in order to collect info about the model
        self._dataset_start_end = self._get_start_and_end_dates(data)

        self._model = SARIMAX(data, order=self._order,
                              seasonal_order=self._seasonal_order,
                              enforce_stationarity=self._enforce_stationary,
                              enforce_invertibility=self._enforce_invertibility)

        self._model_results = self._model.fit()
        
        return self

    def predict(self, steps=48) -> numpy.ndarray:
        """
        Returns a forecast of a given number of steps in the future.

        Parameters
        ----------
        steps : integer
            Number of steps to forecast from the end of the sample.
            It is related to the frequency of the data, so if the data
            has an hourly frequency then the number of steps would be 
            the hours to predict in the future. Default is 48.
        
        Returns
        -------
        forecast : numpy.ndarray
            Array of out-of-sample forecasts
        """
        forecast = self._model_results.get_forecast(steps)
        
        return forecast.predicted_mean

    def get_info(self) -> dict:
        info = {
            'name': 'SARIMA',
            'parameters': {
                'non_seasonal_params': self._order,
                'seasonal_params': self._seasonal_order
            },
            'dataset_start_end': self._dataset_start_end
        }

        return info

class ProphetEstimator(TimeSeriesEstimator):
    """
    This class wraps up a Prophet model into an Estimator.

    Parameters
    ----------
    seasonality_mode : String
        Kind of seasonality, additive or multiplicative.
        Default is additive.
    year_seasonality : String, bool or integer
        Can be 'auto', True, False, or a number of Fourier terms to generate.
        Default is auto
    weekly_seasonality: Fit weekly seasonality.
        Can be 'auto', True, False, or a number of Fourier terms to generate.
        Default is auto
    daily_seasonality: Fit daily seasonality.
        Can be 'auto', True, False, or a number of Fourier terms to generate.
        Default is auto
    
    Attributes
    ----------
    model : Prophet
        Prophet object containing the model. Initialized with default parameters.

    Notes
    -----
    This class extends TimeSeriesEstimator in order to be able to be used
    in sklearn Pipelines and GridSearchCV.
    """

    def __init__(self, seasonality_mode='additive', yearly_seasonality='auto',
                 weekly_seasonality='auto', daily_seasonality='auto'):
        self._seasonality_mode = seasonality_mode              
        self._model = Prophet(seasonality_mode=seasonality_mode,
                              yearly_seasonality=yearly_seasonality,
                              weekly_seasonality=weekly_seasonality,
                              daily_seasonality=daily_seasonality)

        self._dataset_start_end = ''
        
    def fit(self, data: pandas.DataFrame, y=None) -> ProphetEstimator:
        """
        Fits the model with the fiven data.

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame containing the history. Must have columns
            ds (date type) and y (values).
        
        Returns
        -------
        self : ProphetEstimator
            Self ProphetEstimator object with fitted model
        """
        # Gets the start and the end of the dataset in order to collect info about the model
        self._dataset_start_end = self._get_start_and_end_dates(data)

        if 'ds' not in data.columns or 'y' not in data.columns:
            data = data.reset_index()
            data = data.rename(columns={data.columns[0]: "ds", data.columns[1]: "y"})

        self._model = self._model.fit(data)

        return self

    def predict(self, steps=48, freq='H') -> numpy.ndarray:
        """
        Returns a forecast of a given number of steps in the future.

        Parameters
        ----------
        steps : integer
            Number of steps to predict in the future. It is used to create
            the future dataframe. Default is 48.
        freq : String
            Frequency of the future dataframe. Default is 'H', which 
            refers to hourly predictions.
        
        Returns
        -------
        forecast : numpy.ndarray
            DataFrame with forecasted values
        """
        future_df = self._model.make_future_dataframe(periods=steps, freq=freq, include_history=False)

        forecast = self._model.predict(future_df)

        return forecast['yhat'].values

    def get_info(self) -> dict:
        info = {
            'name': 'Prophet',
            'parameters': {
                'seasonality_mode': self._seasonality_mode
            },
            'dataset_start_end': self._dataset_start_end
        }

        return info