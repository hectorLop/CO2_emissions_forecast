import pandas

class ModelEvaluation():
    """
    This class represents a ModelEvaluator to obtain several
    metrics from a model

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing the whole dataset

    Attributes
    ----------
    _data : pandas.DataFrame
        DataFrame containing the whole dataset
    """
    
    def __init__(self, data: pandas.DataFrame) -> None:
        self._data = data

    def cross_validation(self):
        pass