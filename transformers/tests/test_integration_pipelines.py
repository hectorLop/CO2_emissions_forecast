import pytest
from ..preparation_transformers import *
from ..cleaning_transformers import RemoveDateErrors, RemoveDuplicates
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

def test_cleaning_pipeline(supply_pipelines):
    """
    Test the full cleaning pipeline

    Parameters
    ----------
    supply_pipelines : dict
        Dictionary containing the cleaning pipeline
    """
    cleaning_pipeline = supply_pipelines['cleaning']

    original_df = pandas.DataFrame({
        'Dates': ['2020-01-01 01:00', '2020-01-01 01:10',
                '2020-01-01 01:10', '2020-01-01 01:20',
                '2020-01-01 01:20', '2020-01-01 01:30',
                '2020-01-01 01:40', '2020-01-01 01:50',
                '2020-01-01 2A:00', '2020-01-01 2A:10',
                '2020-01-01 2A:20', '2020-01-01 2A:30',
                '2020-01-01 2A:40', '2020-01-01 2A:50',
                '2020-01-01 2B:00', '2020-01-01 2B:10'],
        'Emissions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 16]
    })

    expected_df = pandas.DataFrame({
        'Dates': ['2020-01-01 01:00', '2020-01-01 01:10',
                '2020-01-01 01:20', '2020-01-01 01:30',
                '2020-01-01 01:40', '2020-01-01 01:50',
                '2020-01-01 02:00', '2020-01-01 02:10',
                '2020-01-01 02:20', '2020-01-01 02:30',
                '2020-01-01 02:40', '2020-01-01 02:50'],
        'Emissions': [1, 2, 4, 6, 7, 8, 9, 10, 11,
                    12, 13, 14]
    })

    # Apply yhe pipeline to the data
    cleaned_data = cleaning_pipeline.fit_transform(original_df)
    # Get back a default index
    cleaned_data = cleaned_data.reset_index(drop=True)

    assert_frame_equal(cleaned_data, expected_df)

def test_preparation_pipeline(supply_pipelines):
    """
    Test the full preparation pipeline

    Parameters
    ----------
    supply_pipelines : dict
        Dictionary containing the preparation pipeline
    """
    preparation_pipeline = supply_pipelines['preparation']

    original_df = pandas.DataFrame({
        'Dates': ['2020-01-01 01:00', '2020-01-01 01:10',
                '2020-01-01 01:40', '2020-01-01 01:50',
                '2020-01-01 01:20', '2020-01-01 01:30',
                '2020-01-01 02:00', '2020-01-01 02:10',
                '2020-01-01 02:20', '2020-01-01 02:30',
                '2020-01-01 02:40', '2020-01-01 02:50'],
        'Emissions': [2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5]
    })

    expected_df = pandas.DataFrame({
        'Emissions': [0.693147, 1.609438]
    }, index=pandas.date_range('20200101 01:00:00', freq='H', periods=2))
    # Set the name of the index the same as the name of the date column of original_df
    expected_df.index.name = 'Dates'

    prepared_df = preparation_pipeline.fit_transform(original_df)

    assert_frame_equal(prepared_df, expected_df)

def test_cleaning_and_preparation_pipelines():
    """
    Test both the cleaning and preparation pipeliness
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

    original_df = pandas.DataFrame({
        'Dates': ['2020-01-01 01:00', '2020-01-01 01:10',
                '2020-01-01 01:10', '2020-01-01 01:20',
                '2020-01-01 01:20', '2020-01-01 01:30',
                '2020-01-01 01:40', '2020-01-01 01:50',
                '2020-01-01 2A:00', '2020-01-01 2A:10',
                '2020-01-01 2A:20', '2020-01-01 2A:30',
                '2020-01-01 2A:40', '2020-01-01 2A:50',
                '2020-01-01 2B:00', '2020-01-01 2B:10'],
        'Emissions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 16]
    })