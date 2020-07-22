import pytest
from ..preparation_transformers import *
from ..cleaning_transformers import RemoveDateErrors, RemoveDuplicates
import pandas
from pandas.testing import assert_frame_equal
from sklearn.pipeline import Pipeline

def test_cleaning_pipeline():
    """
    Test the full cleaning pipeline
    """
    cleaning_pipeline = Pipeline([
        ('remove_duplicates', RemoveDuplicates('Dates')),
        ('remove_errors', RemoveDateErrors('Dates'))
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