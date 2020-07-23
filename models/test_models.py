import pytest
from ..transformers.preparation_transformers import *
from ..transformers.cleaning_transformers import RemoveDateErrors, RemoveDuplicates
import pandas
from pandas.testing import assert_frame_equal
from sklearn.pipeline import Pipeline

@pytest.fixture
def supply_pipelines() -> dict:
    """
    Provide a dictionary containing the cleaning and the preparation pipelines
    """
    cleaning_pipeline = Pipeline([
        ('remove_duplicates', RemoveDuplicates('Dates')),
        ('remove_errors', RemoveDateErrors('Dates'))
    ])

    preparation_pipeline = Pipeline([
        ('convert_to_datetime', ConvertToDatetime('Dates')),
        ('sort_by_index', SortByIndex('Dates')),
        ('set_frequency', SetFrequency('10min')),
        ('interpolation', Interpolation()),
        ('resampler', Resampler('H', 'Emissions')),
        ('boxcox', BoxCox('Emissions'))
    ])

    pipelines = {}
    pipelines['cleaning'] = cleaning_pipeline
    pipelines['preparation'] = preparation_pipeline

    return pipelines

def test_arima_estimator(supply_pipelines):
    """
    Test if the ARIMA estimator is capable of yield predictions
    """
    pass

def test_prophet_estimator(supply_pipelines):
    """
    Test if the Prophet estimator is capable of yield predictions
    """
    pass