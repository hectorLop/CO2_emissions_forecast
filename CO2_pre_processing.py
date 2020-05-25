import pandas

def prepare_timeseries_dataset(dataset: pandas.DataFrame, ts_column_pos: int) -> pandas.DataFrame:
    """
    Prepare a time series dataset ready to be processed

    Parameters:
        dataset (pandas.DataFrame): dataset to be prepared
        ts_column_pos (int): position of the timestamp column
    Returns:
        dataset ready to be processed
    """

    ts_column_name = dataset.columns[ts_column_pos]

    # Converts the timestamp column to datetime object
    dataset[ts_column_name] = pandas.to_datetime(dataset[ts_column_name])
    # Sets the timestamp column as index
    dataset = dataset.set_index(ts_column_name)
    # Sort the dataset by index
    dataset = dataset.sort_index()

    return dataset