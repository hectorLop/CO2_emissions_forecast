from __future__ import annotations
from sklearn.base import TransformerMixin
import pandas

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
        self : RemoveDuplicates
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
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> SortByIndex:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

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