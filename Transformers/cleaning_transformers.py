from __future__ import annotations
from sklearn.base import TransformerMixin
import pandas

class RemoveDuplicates(TransformerMixin):
    """
    This class defines a Transformer to remove duplicated dates

    Parameters
    ----------
    column_name : string
        Column name containing duplicates

    Attributes
    ----------
    column_name : string
        Column name containing duplicates
    """

    def __init__(self, column_name: str) -> None:
        self._column_name = column_name

    def fit(self, X: pandas.DataFrame, y=None) -> RemoveDuplicates:
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
        Drop the duplicated dates from given data

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe with the data
        
        Returns
        -------
        X : pandas.DataFrame
            DataFrame containing no duplicated dates
        """
        X = X.drop_duplicates(self._column_name)

        return X

class RemoveDateErrors(TransformerMixin):
    """
    This class defines a Transformer to remove dates errors

    Parameters
    ----------
    column_name : string
        Column name containing errors

    Attributes
    ----------
    column_name : string
        Column name containing errors
    """

    def __init__(self, column_name: str) -> None:
        self._column_name = column_name

    def fit(self, X: pandas.DataFrame, y=None) -> RemoveDateErrors:
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

    def transform(self, X: pandas.DataFrame, y=None) -> pandas.DataFrame:
        """
        Remove dates errors from given data

        Parameters
        ----------
        X : pandas.DataFrame
            Dataframe with the data
        
        Returns
        -------
        X : pandas.DataFrame
            DataFrame that contains no errors
        """
        # Creates a deep copy to avoid a CopyWarning
        new_dataset = X.copy()

        # Condition to get all dates containing '2A'
        condition = new_dataset[self._column_name].str.contains('2A')
        # Replace 2A by 02 on dates matching the condition
        new_dataset.loc[condition, self._column_name] = new_dataset.loc[condition, self._column_name].str.replace('2A', '02')
        # Use the NOT simbol (~) to return the dataset without rows containing a 2B
        new_dataset = new_dataset[~new_dataset[self._column_name].str.contains("2B")]

        return new_dataset