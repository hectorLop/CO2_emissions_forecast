from sklearn.base import TransformerMixin
import pandas

class RemoveDuplicates(TransformerMixin):
    """
    This class defines a Transformer to remove duplicated dates

    Parameters
    ----------
    column_name : string
        Column name which contains duplicates

    Attributes
    ----------
    column_name : string
        Column name which contains duplicates
    """

    def __init__(self, column_name: str) -> None:
        self._column_name = column_name

    def fit(self, X: pandas.DataFrame, y=None):
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
        Drop the duplicated dates from the given data

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

class RemoveErrors(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X, y=None):
        pass

    def transform(self, X, y=None):
        pass