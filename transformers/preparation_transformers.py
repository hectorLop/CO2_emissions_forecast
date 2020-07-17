from __future__ import annotations
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
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> SetFrequency:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

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