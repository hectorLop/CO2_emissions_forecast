import pytest
import pandas

@pytest.fixture
def supply_df() -> pandas.DataFrame:
    """
    Supply a test dataframe
    """
    # Use this path due to the tests are executed from the main directory
    df = pandas.read_csv('Test_Dataset_2020_01_01_to_2020_02_29.csv')

    # Converts the dates column to datetime object and sets it as the index 
    df['Fecha'] = pandas.to_datetime(df['Fecha'])
    df = df.set_index('Fecha')

    # Sets the dataset frequency
    df.index.freq = pandas.infer_freq(df.index)

    return df