import pytest
from ..preparation_transformers import *
from pandas.testing import assert_frame_equal, assert_index_equal
import pandas
import numpy
from datetime import datetime
from numpy.testing import assert_equal

@pytest.fixture
def supply_unordered_dates():
    """
    Creates a dictionary containing unordered dates as string and as objects
    """
    dates_str = ['2020-01-01 21:00', '2020-01-01 22:00',
                '2020-01-01 23:00', '2020-01-01 20:00']
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M') for date in dates_str]

    dates_dict = {}
    dates_dict['dates_str'] = dates_str
    dates_dict['dates'] = dates

    return dates_dict

@pytest.fixture
def supply_sorted_dates():
    """
    Creates a dictionary containing sorted dates as strings and as objects
    """
    sorted_dates_str = ['2020-01-01 20:00', '2020-01-01 21:00',
                        '2020-01-01 22:00', '2020-01-01 23:00']
    sorted_dates = [datetime.strptime(date, '%Y-%m-%d %H:%M') for date in sorted_dates_str]

    sorted_dates_dict = {}
    sorted_dates_dict['sorted_dates_str'] = sorted_dates_str
    sorted_dates_dict['sorted_dates'] = sorted_dates

    return sorted_dates_dict

@pytest.fixture
def supply_df():
    """
    Creates a dictionary containing two data frames, the first with
    a frequency of 10 minutes and the last with a frequency of 1 hour.
    """
    # Creates the emissions values and the dates with 10min frequency
    emissions_values = [2, 2, 2, 2, 2, 2, 5, 5, 5, 5 ,5, 5]
    dates_by_10_min = pandas.date_range('20200101 20:00:00', freq='10T', periods=12)

    minutes_dataframe = pandas.DataFrame({
        'Emissions': emissions_values
    }, index=dates_by_10_min)

    # Creates the emissions mean and the dates with 1 hour frequency
    mean_emissions = [2, 5]
    dates_by_hour = pandas.date_range('20200101 20:00:00', freq='H', periods=2)

    hourly_dataframe = pandas.DataFrame({
        'Emissions': mean_emissions
    }, index=dates_by_hour)

    dataframes_dict = {}
    dataframes_dict['minutes_dataframe'] = minutes_dataframe
    dataframes_dict['hourly_dataframe'] = hourly_dataframe

    return dataframes_dict

def test_convert_to_datetime(supply_unordered_dates) -> None:
    """
    Test the ConvertToDatetime transformer

    Parameters
    ----------
    supply_unordered_dates : dict
        Dictionary containing unordered dates as strings and as objects
    """
    # Creates both datasets
    original_dataset = pandas.DataFrame({
        'Dates': supply_unordered_dates['dates_str'],
        'Emissions': [1500, 1512, 1583, 1541]
    })

    expected_dataset = pandas.DataFrame({
        'Dates': supply_unordered_dates['dates'],
        'Emissions': [1500, 1512, 1583, 1541]
    })

    convert_to_datetime = ConvertToDatetime('Dates')

    result = convert_to_datetime.fit_transform(original_dataset)

    assert_frame_equal(expected_dataset, result)

def test_sort_by_index(supply_unordered_dates, supply_sorted_dates):
    """
    Test the SortByIndex transformer

    Parameters
    ----------
    supply_unordered_dates : dict
        Dictionary containing unordered dates as strings and as objects
    
    supply_sorted_dates : dict
        Dictionary containing sorted dates as strings and as objects
    """  
    # Creates the original dataset without the DatetimeIndex
    original_dataset = pandas.DataFrame({
        'Dates': supply_unordered_dates['dates'],
        'Emissions': [1500, 1512, 1583, 1541]
    })

    # Creates the expected dataframe with the sorted dates as index
    expected_dataset = pandas.DataFrame({
        'Emissions': [1541, 1500, 1512, 1583]
    }, index=supply_sorted_dates['sorted_dates'])

    # Set the index name to be equal as the original dataset
    expected_dataset.index.name = 'Dates'

    sort_by_index = SortByIndex('Dates')

    result = sort_by_index.fit_transform(original_dataset)

    assert_frame_equal(result, expected_dataset)

def test_set_frequency(supply_sorted_dates):
    """
    Test the SetFrequency transformer

    Parameters
    ----------
    supply_sorted_dates : dict
        Dictionary containing sorted dates as strings and as objects
    """
    # Creates the original dataframe with a DatetimeIndex and no frequency
    original_dataset = pandas.DataFrame({
        'Emissions': [1541, 1500, 1512, 1583]
    }, index=supply_sorted_dates['sorted_dates'])

    set_frequency = SetFrequency('10min')

    result = set_frequency.fit_transform(original_dataset)

    # Get the frequency string from the index
    result_frequency = result.index.freq.freqstr
    expected_frequency = '10T'

    assert expected_frequency == result_frequency 

def test_interpolation(supply_sorted_dates):
    """
    Test the Interpolation transformer

    Parameters
    ----------
    supply_sorted_dates : dict
        Dictionary containing sorted dates as strings and as objects
    """
    # Creates the original dataframe containing missing values
    original_dataset = pandas.DataFrame({
        'Emissions': [1541, numpy.nan, 1512, numpy.nan]
    }, index=supply_sorted_dates['sorted_dates'])

    interpolation = Interpolation()

    result = interpolation.fit_transform(original_dataset)
    # Gets the number of nans from the Emissions column, index 0
    number_of_nans = result.isnull().sum()[0]

    assert_equal(number_of_nans, 0)

def test_Resampler(supply_df):
    """
    Test the Resampler transformer

    Parameters
    ----------
    supply_df : dict
        Dictionary containing two data frames, the first with a frequency
        of 10 minutes and the last with a frequency of 1 hour.
    """
    original_dataset = supply_df['minutes_dataframe']

    resampler = Resampler('H', 'Emissions')

    result = resampler.fit_transform(original_dataset)

    assert_frame_equal(result, supply_df['hourly_dataframe'])

def test_BoxCox(supply_df):
    """
    Test the BoxCox transformer

    Parameters
    ----------
    supply_df : dict
        Dictionary containing two data frames, the first with a frequency
        of 10 minutes and the last with a frequency of 1 hour.
    """
    original_dataset = supply_df['hourly_dataframe']

    expected_dataset = pandas.DataFrame({
        'Emissions': [0.693147, 1.609438]
    }, index=pandas.date_range('20200101 20:00:00', freq='H', periods=2))

    box_cox = BoxCox('Emissions')

    result = box_cox.fit_transform(original_dataset)

    assert_frame_equal(expected_dataset, result)