import pytest
from ..preparation_transformers import *
from pandas.testing import assert_frame_equal, assert_index_equal
import pandas
import numpy
from datetime import datetime

def test_convert_to_datetime():
    """
    Test the ConvertToDatetime transformer
    """
    # Creates both the dates as strings and as datetime objects
    dates_str = ['2020-01-01 21:00', '2020-01-01 22:00',
                '2020-01-01 23:00', '2020-01-01 21:00']
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M') for date in dates_str]

    original_dataset = pandas.DataFrame({
        'Dates': dates_str,
        'Emissions': [1500, 1512, 1583, 1541]
    })

    expected_dataset = pandas.DataFrame({
        'Dates': dates,
        'Emissions': [1500, 1512, 1583, 1541]
    })

    convert_to_datetime = ConvertToDatetime('Dates')

    result = convert_to_datetime.fit_transform(original_dataset)

    assert_frame_equal(expected_dataset, result)

def test_sort_by_index():
    """
    Test the SortByIndex transformer
    """
    # Creates a list with unsorted dates
    dates_str = ['2020-01-01 21:00', '2020-01-01 22:00',
                '2020-01-01 23:00', '2020-01-01 20:00']
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M') for date in dates_str]

    # Creates the original dataset without the DatetimeIndex
    original_dataset = pandas.DataFrame({
        'Dates': dates,
        'Emissions': [1500, 1512, 1583, 1541]
    })

    # Creates a list with sorted dates
    sorted_dates_str = ['2020-01-01 20:00', '2020-01-01 21:00',
                        '2020-01-01 22:00', '2020-01-01 23:00']
    sorted_dates = [datetime.strptime(date, '%Y-%m-%d %H:%M') for date in sorted_dates_str]

    # Creates the expected dataframe with the sorted dates as index
    expected_dataset = pandas.DataFrame({
        'Emissions': [1541, 1500, 1512, 1583]
    }, index=sorted_dates)

    # Set the index name to be equal as the original dataset
    expected_dataset.index.name = 'Dates'

    sort_by_index = SortByIndex('Dates')

    result = sort_by_index.fit_transform(original_dataset)

    assert_frame_equal(result, expected_dataset)

def test_set_frequency():
    """
    Test the SetFrequency transformer
    """
    pass

def test_interpolation():
    """
    Test the Interpolation transformer
    """
    pass

def test_Resampler():
    """
    Test the Resampler transformer
    """
    pass

def test_BoxCox():
    """
    Test the BoxCox transformer
    """
    pass