from models.custom_estimators import ARIMAEstimator, ProphetEstimator
import pandas

class ModelTrainer():
    """
    This class represents a ModelTrainer to obtain the best
    possible model and its parameters

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

    def __init__(self) -> None:
        self._train_data = None
        self._test_data = None

    def grid_search(train_data: pandas.DataFrame, test_data: pandas.DataFrame) -> dict:
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

    def __generate_train_and_test_sets(data: pandas.DataFrame) -> tuple:
        """
        Split the data into train and test sets

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame containing the whole dataset

        Returns
        -------
        train_data, test_data : tuple(pandas.DataFrame)
            Two DataFrames containing the train and test data
        """
        pass

    def __grid_search_ARIMA(train_data: pandas.DataFrame, test_data: pandas.DataFrame) -> dict:
        """
        Apply GridSearch with an ARIMA model to obtain the model's best parameters

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

    def __grid_search_Prophet(train_data: pandas.DataFrame, test_data: pandas.DataFrame) -> dict:
        """
        Apply GridSearch with a Prophet model to obtain the model's best parameters

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