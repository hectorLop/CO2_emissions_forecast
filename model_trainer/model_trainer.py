from .grid_search import GridSearch, ARIMAGridSearch, ProphetGridSearch
from typing import Tuple
import pandas

class ModelTrainer():
    """
    This class represents a ModelTrainer to obtain the best
    possible model and its parameters

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing the whole data

    Attributes
    ----------
    _train_data : pandas.DataFrame
        DataFrame containing the training data

    _test_data : pandas.DataFrame
        DataFrame containing the test data

    Models List
    -----------
    - SARIMA
    - FBProphet
    """

    def __init__(self, data: pandas.DataFrame) -> None:
        self._train_data, self._test_data = self.__generate_train_and_test_sets(data)

    def grid_search(self, train_data: pandas.DataFrame, test_data: pandas.DataFrame) -> dict:
        """
        Apply GridSearch on different models to obtain the best one

        Parameters
        ----------
        train_data : pandas.DataFrame
            DataFrame containing the training data for the model

        test_data : pandas.DataFrame
            DataFrame containing the test data for the model

        Returns
        -------
        results : dict
            Dictionary containing the best model with its parameters and metrics
        """
        pass

    def __generate_train_and_test_sets(self, data: pandas.DataFrame) -> Tuple[pandas.DataFrame, pandas.DataFrame]:
        """
        Split the data into train and test sets

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame containing the whole dataset

        Returns
        -------
        train_data, test_data : tuple(pandas.DataFrame, pandas.DataFrame)
            Two DataFrames containing the train and test data
        """
        # Assuming hourly frequency, the train data is the full dataset less 2 days
        # which are the test data
        train_data = data.iloc[:-48, :].copy()
        test_data = data.iloc[-48:, :].copy()

        return train_data, test_data