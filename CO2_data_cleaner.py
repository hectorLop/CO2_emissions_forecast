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

        # Removes the unnamed column
        dataset = self.__remove_unnamed_column(dataset)
        # Removes duplicated dates
        dataset = dataset.drop_duplicates("Fecha")
        # Removes the date errors
        dataset = self.__remove_date_errors(dataset)

        return dataset

    def __remove_unnamed_column(self, dataset: pandas.DataFrame) -> pandas.DataFrame:
        """
        Removes the 'Unnamed: 0' column if it exists
           
        Parameters:
            dataset (pandas.DataFrame): datatest which may contain an Unnamed: 0 column
        Returns:
            Cleaned dataset as pandas.DataFrame
        """

        # Drop the Unnamed: 0 column
        if 'Unnamed: 0' in dataset.columns:
            dataset = dataset.drop(['Unnamed: 0'], axis=1)

        return dataset

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

        # Replace dates with 2A by 02
        dataset['Fecha'] = dataset['Fecha'].str.replace('2A', '02')
        # Use the NOT simbol (~) to return the dataset without rows containing a 2B
        dataset = dataset[~dataset.Fecha.str.contains("2B")]

        return dataset
