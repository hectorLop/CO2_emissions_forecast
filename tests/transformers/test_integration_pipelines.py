import pytest
from source.transformers.preparation_transformers import *
from source.transformers.cleaning_transformers import RemoveDateErrors, RemoveDuplicates
import pandas
from pandas.testing import assert_frame_equal
from sklearn.pipeline import Pipeline
from tests.tests_fixtures.fixtures import supply_pipelines

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

    # Applies the pipeline to the data
    cleaned_data = cleaning_pipeline.fit_transform(original_df)
    # Gets back a default index
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
    # Sets the name of the index the same as the name of the date column in original_df
    expected_df.index.name = 'Dates'

    prepared_df = preparation_pipeline.fit_transform(original_df)

    assert_frame_equal(prepared_df, expected_df)

def test_cleaning_and_preparation_pipelines(supply_pipelines):
    """
    Test both the cleaning and preparation pipelines combined

    Parameters
    ----------
    supply_pipelines : dict
        Dictionary containing both pipelines
    """
    combined_pipeline = Pipeline([
        ('cleaning', supply_pipelines['cleaning']),
        ('preparation', supply_pipelines['preparation'])
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
        'Emissions': [2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5,
                    5, 5, 5, 8, 8]
    })

    expected_df = pandas.DataFrame({
        'Emissions': [0.693147, 1.609438]
    }, index=pandas.date_range('20200101 01:00:00', freq='H', periods=2))
    # Sets the name of the index the same as the name of the date column in original_df
    expected_df.index.name = 'Dates'

    result = combined_pipeline.fit_transform(original_df)

    assert_frame_equal(result, expected_df)