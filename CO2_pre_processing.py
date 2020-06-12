import pandas
from datetime import datetime
import numpy
import sklearn.metrics as metrics
from typing import Dict

class CO2DataPreparation():
    """
    This class models the data preparation pipeline for the CO2 problem
    Prepares the CO2 dataset to be used in a predictive model
    """

    def __init__(self):
        pass

    def create_dataset_timefreq_1hour(self, dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Creates a dataset where the difference between timestamps is 1 hour

        Parameters:
            dataset (pandas.DataFrame): Dataset where difference between timestamps is not 1 hour
        Returns:
            New dataset with a difference of 1 hour between timestamps and values grouped by each hour
        """

        # Creates the new dataset
        dataset_freq_1hour = pandas.DataFrame()

        # If the dataset has an index different from pandas default RangeIndex, it is reset
        dataset = self.__reset_index_if_no_RangeIndex(dataset)

        # Creates 'Fecha' column with custom datetime
        dataset_freq_1hour['Fecha'] = dataset['Fecha'].apply(self.__create_date_with_no_minutes_and_seconds).unique()

        # Converts Fecha column into DatetimeIndex in order to group emissions by hours
        times = pandas.DatetimeIndex(dataset.Fecha)
        # Creates dataset  grouped by hour
        # Parameter 'as_index = False' needed in order to be able to obtain the values
        dataset_grouped_by_hour = dataset.groupby([times.year, times.month, times.day, times.hour], as_index=False)
        
        # Creates 'Emisiones' column with the emissions sum for each hour
        dataset_freq_1hour['Emisiones'] = dataset_grouped_by_hour.sum()['Emisiones']

        return dataset_freq_1hour

    def __reset_index_if_no_RangeIndex(self, dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Reset the dataset index if it is not a RangeIndex, which is the default pandas index

        Parameters:
            dataset (pandas.DataFrame): dataset to be checked
        Returns:
            Dataset with reset index if true
        """

        if dataset.index != pandas.RangeIndex:
            return dataset.reset_index()
        
        return dataset

    def __create_date_with_no_minutes_and_seconds(self, datetime_value: pandas.Series) -> datetime:
        """
        Creates a datetime with year, month, day and hour from a full timestamp

        Parameters:
            row (pandas.Series): Row of the dataset
        Returns:
            Datetime with year, month, day and hour
        """

        year = datetime_value.year
        month = datetime_value.month
        day = datetime_value.day
        hour = datetime_value.hour

        return datetime(year, month, day, hour)

    def prepare_timeseries_dataset(self, dataset: pandas.DataFrame, ts_column_position: int) -> pandas.DataFrame:
        """
        Prepare a time series dataset ready to be processed

        Parameters:
            dataset (pandas.DataFrame): dataset to be prepared
            ts_column_pos (int): position of the timestamp column
        Returns:
            dataset ready to be processed
        """

        ts_column_name = dataset.columns[ts_column_position]

        # Converts the timestamp column to datetime object
        dataset[ts_column_name] = pandas.to_datetime(dataset[ts_column_name])
        # Sets the timestamp column as index
        dataset = dataset.set_index(ts_column_name)
        # Sort the dataset by index
        dataset = dataset.sort_index()

        return dataset

    def change_frequency(self, dataset: pandas.DataFrame, frequency: str) -> pandas.DataFrame:
        """
        Change the frequency of a given dataset.

        Parameters:
            dataset (pandas.DataFrame): Dataset to be setted a new frequency
            frequency (str): Offset alias representing the frequency desired
        Return:
            Dataset with new frequency
        """
        
        # Set new frequency to the data
        dataset = dataset.asfreq(frequency)

        # The new frequency may have created missing values, so they must be handled
        dataset = self.__handle_missing_values(dataset)
        
        return dataset
  
    def create_resampled_dataset(self, dataset: pandas.DataFrame, freq_to_resample: str) -> pandas.DataFrame:
        """
        Resample a dataset with a custom frequency

        Parameters:
            dataset (pandas.DataFrame): Dataset to be resampled
            freq_to_resample (str): Offset alias to resample the dataset
        Returns:
            New dataset with custom frequency
        """

        # Check if dataset has frequency in order to prevent errors
        if dataset.index.freq is None:
            return None

        # Resample the dataset with a new frequency
        new_series = dataset['Emisiones'].resample(freq_to_resample).sum()

        # Creates new dataset from the resampled series
        new_dataset = pandas.DataFrame({'Emisiones':new_series.values}, index=new_series.index)

        return new_dataset

    def __handle_missing_values(self, dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Handle the missing values if they exist in a given dataset

        Parameters:
            dataset (pandas.DataFrame): Dataset to with possible missing values
        Returns:
            Dataset without missing values
        """

        missing_values = dataset.isnull().sum()

        if missing_values > 0:
            # Use linear interpolation to fill missing values
            dataset = dataset.interpolate()
        
        return dataset


def regression_perfomance_metrics(real_values: pandas.Series, predicted_values: pandas.Series) -> Dict[str, float]:
    """
    Gets the following regression metrics: MAE, MSE, RMSE, R^2 and MAPE for given real and predicted values

    Parameters:
        - real_values (pandas.Series): Real values of data
        - predicted_values (pandas.Series): Predicted values of data
    Returns:
        List with all the metrics in this order:
            0 -> MAE
            1 -> MSE
            2 -> RMSE
            3 -> R^2
            4 -> MAPE
    """

    regression_metrics = {}

    # Convert Series to numpy arrays
    real_values = real_values.to_numpy()
    predicted_values = predicted_values.to_numpy()

    # MAE calculation
    mean_absolute_error = metrics.mean_absolute_error(real_values, predicted_values)
    regression_metrics['MAE'] = mean_absolute_error

    # MSE calculation
    mean_squared_error = metrics.mean_squared_error(real_values, predicted_values)
    regression_metrics['MSE'] = mean_squared_error

    # RMSE calculation
    rooted_mean_squared_error = numpy.sqrt(mean_squared_error)
    regression_metrics['RMSE'] = rooted_mean_squared_error

    # R^2 calculation
    r2_score = metrics.r2_score(real_values, predicted_values)
    regression_metrics['R^2'] = r2_score

    # MAPE calculation
    mean_absolute_percentage_error = numpy.mean(
        numpy.abs((real_values - predicted_values) / real_values)) * 100
    regression_metrics['MAPE'] = mean_absolute_percentage_error

    return regression_metrics