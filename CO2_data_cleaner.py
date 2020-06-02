import pandas

class CO2DataCleaner:
    """
    This class models the Data Cleaner for this specific problem.
    Cleans the data related to CO2 emissions. 
    """

    def __init__(self):
        pass
    
    def clean_data(self, dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Cleans the data from errors and inconsistencies

        Parameters:
            dataset (pandas.DataFrame): data to be cleaned
        Returns:
            Cleaned dataset as pandas.DataFrame
        """

        return None

    def __remove_unnamed_column(self, dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Removes the 'Unnamed: 0' column if it exists
           
        Parameters:
            dataset (pandas.DataFrame): datatest which may contain an Unnamed: 0 column
        Returns:
            Cleaned dataset as pandas.DataFrame
        """

        return None

    def __remove_date_errors(self, dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Removes errors in the dataset
        Some dates at 02:00am have the following format:
            2019-10-27 2A:40
            2019-10-27 2A:50
            2019-10-27 2B:00
            2019-10-27 2B:10 

        Parameters:
            dataset (pandas.DataFrame): data which may contain dates errors
        Returns:
            Cleaned dataset as pandas.DataFrame
        """

        return None
