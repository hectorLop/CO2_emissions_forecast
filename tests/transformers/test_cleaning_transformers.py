import pytest
from source.transformers.cleaning_transformers import RemoveDateErrors, RemoveDuplicates
from pandas.testing import assert_frame_equal
import pandas

def test_remove_duplicates():
    """
    Test the RemoveDuplicates transformer
    """
    original_dataset = pandas.DataFrame({
        'Dates': ['2020-01-01 21:00', '2020-01-01 22:00',
                '2020-01-01 23:00', '2020-01-01 21:00'],
        'Emissions': [1500, 1512, 1583, 1541]
    })

    expected_dataset = pandas.DataFrame({
        'Dates': ['2020-01-01 21:00', '2020-01-01 22:00',
                '2020-01-01 23:00'],
        'Emissions': [1500, 1512, 1583]
    })

    remove_duplicates = RemoveDuplicates('Dates')

    result = remove_duplicates.fit_transform(original_dataset)

    assert_frame_equal(expected_dataset, result)

def test_remove_date_errors():
    """
    Test the RemoveDuplicates transformer
    """
    original_dataset = pandas.DataFrame({
        'Dates': ['2020-01-01 01:40', '2020-01-01 01:50',
                '2020-01-01 2A:00', '2020-01-01 2A:10',
                '2020-01-01 2A:20', '2020-01-01 2A:30',
                '2020-01-01 2A:40', '2020-01-01 2A:50',
                '2020-01-01 2B:00', '2020-01-01 2B:10'],
        'Emissions': [1500, 1512, 1583, 1541, 1500, 1512,
                     1583, 1541, 1600, 1700]
    })

    expected_dataset = pandas.DataFrame({
        'Dates': ['2020-01-01 01:40', '2020-01-01 01:50',
                '2020-01-01 02:00', '2020-01-01 02:10',
                '2020-01-01 02:20', '2020-01-01 02:30',
                '2020-01-01 02:40', '2020-01-01 02:50'],
        'Emissions': [1500, 1512, 1583, 1541, 1500, 1512,
                     1583, 1541]
    })

    remove_errors = RemoveDateErrors('Dates')

    result = remove_errors.fit_transform(original_dataset)

    assert_frame_equal(expected_dataset, result)