import pandas
from ..model_trainer.grid_search import ARIMAGridSearch, ProphetGridSearch
from ..model_trainer.model_trainer import ModelTrainer
from typing import List
import numpy

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

    MODELS_LIST = [ARIMAGridSearch(), ProphetGridSearch()]

    def __init__(self, data: pandas.DataFrame) -> None:
        self._data = data

    def select_best_model(self) -> dict:
        """
        Selects the best possible model from a list of models
        """
        model_trainer = None
        best_model = {}
        results_list = []

        # Obtain the best parameters for each model
        for model in MODELS_LIST:
            model_trainer = ModelTrainer(self._data, model)

            results_list.append(model_trainer.grid_search())
        
        # Obtain the best model
        best_model = self._compare_models(results_list)

        return best_model

    def _compare_models(self, results_list: List[dict]) -> dict:
        """
        Compare the grid search results and returns the best one

        Parameters
        ----------
        results_list : List[dict]
            List of results for each grid search
        """
        best_model = None
        best_mae = numpy.inf

        for results in results_list:
            if results['MAE'] < best_mae:
                best_mae = results['MAE']
                best_model = results
        
        return best_model