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

    def prepare_timeseries_dataset(self, dataset: pandas.DataFrame, ts_column_name: str) -> pandas.DataFrame:
        """
        Prepare a time series dataset ready to be processed

        Parameters:
            dataset (pandas.DataFrame): dataset to be prepared
            ts_column_pos (int): position of the timestamp column
        Returns:
            dataset ready to be processed
        """

        if ts_column_name not in dataset.columns:
            raise ValueError("Given column doesn't appear in the dataset")

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
  
    def create_resampled_dataset(self, dataset: pandas.DataFrame, frequency: str) -> pandas.DataFrame:
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
            raise TypeError("Dataset frequency is None")

        # Resample the dataset with a new frequency
        new_series = dataset['Emisiones'].resample(frequency).sum()

        # Creates new dataset from the resampled series
        new_dataset = pandas.DataFrame({'Emisiones':new_series.values}, index=new_series.index)

        # Resampling may have created missing values
        new_dataset = self.__handle_missing_values(new_dataset)

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