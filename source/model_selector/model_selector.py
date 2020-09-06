import pandas
import numpy

from model_trainer.grid_search import ARIMAGridSearch, ProphetGridSearch
from model_trainer.model_trainer import ModelTrainer
from typing import List
from models.custom_estimators import TimeSeriesEstimator

class ModelSelector():
    """
    This class represents a ModelSelector to train differents models
    with several combinations of parameters in order to obtain the
    best one

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing the whole dataset

    Attributes
    ----------
    _data : pandas.DataFrame
        DataFrame containing the whole dataset
    
    best_params : dict
        Dictionary containint the best model and its parameters
    """
    # Constant list containing the available models
    MODELS_LIST = [ARIMAGridSearch(), ProphetGridSearch()]

    def __init__(self, data: pandas.DataFrame) -> None:
        self._data = data

    def select_best_model(self) -> TimeSeriesEstimator:
        """
        Selects the best possible model from a list of models

        Returns
        -------
        best_model : dict
            Dictionary containing the best model and its parameters
        """
        results_list = []

        # Obtain the best parameters for each model
        for model in self.MODELS_LIST:
            model_trainer = ModelTrainer(self._data, model)
            results = model_trainer.grid_search()
            results_list.append(results)
        
        # Obtain the best model
        best_model = self._select_best_results(results_list)

        return best_model['Model']

    def _select_best_results(self, results_list: List[dict]) -> dict:
        """
        Compare the grid search results and returns the best one

        Parameters
        ----------
        results_list : List[dict]
            List of results for each grid search

        Returns
        -------
        best_results : dict
            Dictionary containing the best model and its results
        """
        best_results = None
        best_mae = numpy.inf

        for results in results_list:
            if results['MAE'] < best_mae:
                best_mae = results['MAE']
                best_results = results
        
        return best_results