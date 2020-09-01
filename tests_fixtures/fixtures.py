import pytest
import pandas
from sklearn.pipeline import Pipeline
from ..transformers.preparation_transformers import *
from ..transformers.cleaning_transformers import RemoveDateErrors, RemoveDuplicates

@pytest.fixture
def supply_df() -> pandas.DataFrame:
    """
    Supplies a test dataframe
    """
    # Use this path due to the tests are executed from the main directory
    df = pandas.read_csv('Test_Dataset_2020_01_01_to_2020_02_29.csv')

    # Converts the dates column to datetime object and sets it as the index 
    df['Fecha'] = pandas.to_datetime(df['Fecha'])
    df = df.set_index('Fecha')

    # Sets the dataset frequency
    df.index.freq = pandas.infer_freq(df.index)

    return df

@pytest.fixture
def supply_pipelines() -> dict:
    """
    Provides a dictionary containing the cleaning and the preparation pipelines
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