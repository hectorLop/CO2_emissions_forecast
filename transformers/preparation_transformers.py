from __future__ import annotations
from typing import Type
from sklearn.base import TransformerMixin
import pandas
import numpy

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
        self : SortByIndex
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
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> Interpolation:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

class Resampler(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> Resampler:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

class BoxCox(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> BoxCox:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass