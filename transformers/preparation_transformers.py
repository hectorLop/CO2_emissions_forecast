from __future__ import annotations
from typing import Type
from sklearn.base import TransformerMixin
import pandas
from scipy.stats import boxcox
from scipy.special import inv_boxcox

class ConvertToDatetime(TransformerMixin):
    """
    This class defines a Transformer to convert the date's column elements from
    a string to a datetime object

    Parameters
    ----------
    column_name : string
        Name of the column containing the dates

    Attributes
    ----------
    column_name : string
        Name of the column containing the dates
    """

    def __init__(self, column_name: str) -> None:
        self._column_name = column_name

    def fit(self, X: pandas.DataFrame, y=None) -> ConvertToDatetime:
        """
        Standard behaviour for fit methods

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe with the data
        
        Returns
        -------
        self : ConvertToDatetime
            Self object
        """
        return self

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        """
        Convert the date's column elements from string to datetime

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame with the data

        Returns
        -------
        X : pandas.DataFrame
            DataFrame with the date's column elements as datetime objects 
        """
        X[self._column_name] = pandas.to_datetime(X[self._column_name])

        return X

class SortByIndex(TransformerMixin):
    """
    This class defines a Transformer to sort the dataset by the index, which 
    is the date's column.

    Parameters
    ----------
    column_name : string
        Name of the column containing the dates

    Attributes
    ----------
    column_name : string
        Name of the column containing the dates
    """

    def __init__(self, column_name: str) -> None:
        self._column_name = column_name

    def fit(self, X: pandas.DataFrame, y=None) -> SortByIndex:
        """
        Standard behaviour for fit methods

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe with the data
        
        Returns
        -------
        self : SortByIndex
            Self object
        """
        return self

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        """
        Sort the dataset by index

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame with the data

        Returns
        -------
        X : pandas.DataFrame
            DataFrame sorted by the index
        """
        if not isinstance(X.index, pandas.DatetimeIndex):
            # Set the datetime column as the index
            X = X.set_index(self._column_name)

        X = X.sort_index()

        return X

class SetFrequency(TransformerMixin):
    """
    This class defines a Transformer set a frequency to the
    datetime index of the dataset.

    The frequency is the time difference between observations.

    Parameters
    ----------
    frequency : string
        Observation's frequency

    Attributes
    ----------
    frequency : string
        Observation's frequency
    """

    def __init__(self, frequency: str) -> None:
        self._frequency = frequency

    def fit(self, X: pandas.DataFrame, y=None) -> SetFrequency:
        """
        Standard behaviour for fit methods

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe with the data
        
        Returns
        -------
        self : SetFrequency
            Self object
        """
        return self

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        """
        Set a frequency on the dataset

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame without index frequency

        Returns
        -------
        X : pandas.DataFrame
            DataFrame with index frequency
        """
        if not isinstance(X.index, pandas.DatetimeIndex):
            raise TypeError('Index must be a DatetimeIndex')
        
        # Convert the timeseries to the given frequency
        X = X.asfreq(self._frequency)

        return X

class Interpolation(TransformerMixin):
    """
    This class defines a Transformer to impute the missing values
    using interpolation

    The frequency is the time difference between observations.
    """

    def __init__(self) -> None:
        self._exist_missing_values = False

    def fit(self, X: pandas.DataFrame, y=None) -> Interpolation:
        """
        Check the existence of missing values

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe with the data
        
        Returns
        -------
        self : Interpolation
            Self object
        """
        # Get a series with the missing values for each column
        missing_values = X.isnull().sum()

        # Iterate through the series to check the missing values of each column
        for index, value in missing_values.iteritems():
            if value != 0:
                self._exist_missing_values = True
                break

        return self

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        """
        Imputes the missing values using interpolation

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame containing missing values

        Returns
        -------
        X : pandas.DataFrame
            DataFrame without missing values
        """
        if self._exist_missing_values:
            # Interpolation using time method
            X = X.interpolate(method='time')

        return X

class Resampler(TransformerMixin):
    """
    This class defines a Transformer to resample time-series data

    Parameters
    ----------
    frequency : str
        The offset string representing target conversion

    column_name: str
        Column's name to be resampled

    Attributes
    ----------
    frequency : str
        The offset string representing target conversion

    column_name: str
        Column's name to be resampled
    """

    def __init__(self, frequency: str, column_name: str) -> None:
        self._frequency = frequency
        self._column_name = column_name

    def fit(self, X: pandas.DataFrame, y=None) -> Resampler:
        """
        Standard behaviour for fit methods

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe with the data
        
        Returns
        -------
        self : Resampler
            Self object
        """
        return self

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        """
        Resample time-series data

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame containing the original data

        Returns
        -------
        X : pandas.DataFrame
            DataFrame containing resampled data
        """
        # Create the series containing the resampled data
        new_series = X[self._column_name].resample(self._frequency).mean()
        # Creates the new dataframe
        new_dataset = pandas.DataFrame({self._column_name:new_series.values}, index=new_series.index)

        return new_dataset

class BoxCox(TransformerMixin):
    """
    This class defines a Transformer to apply BoxCox transformation
    to the data

    Parameters
    ----------
    column_name : str
        Elements Column's name to be transformed

    Attributes
    ----------
    lambda : float
        Scalar that maximizes the log-likelihood function
    column_name : str
        Elements Column's name to be transformed
    """

    def __init__(self, column_name: str) -> None:
        self._lambda = 0.0
        self._column_name = column_name

    def fit(self, X: pandas.DataFrame, y=None) -> BoxCox:
        """
        Standard behaviour for fit methods

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe with the data
        
        Returns
        -------
        self : BoxCox
            Self object
        """
        return self

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        """
        Apply the BoxCox transformation to the data

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame containing the original data

        Returns
        -------
        X : pandas.DataFrame
            DataFrame containing transformed data
        """
        # Apply the transformation and learn the lambda 
        X[self._column_name], self._lambda = boxcox(X[self._column_name])

        return X

    def inverse_transform(self, X: pandas.DataFrame, lambda: float) -> pandas.DataFrame:
        """
        Revert the data to its original form

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame containing transformed data

        Returns
        -------
        X : pandas.DataFrame
            DataFrame containing the original data
        """
        # Apply the transformation and learn the lambda 
        X[self._column_name] = inv_boxcox(X[self._column_name], self._lambda)

        return X