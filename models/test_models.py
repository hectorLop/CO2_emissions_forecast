import pytest
from ..transformers.preparation_transformers import *
from ..transformers.cleaning_transformers import RemoveDateErrors, RemoveDuplicates
import pandas
from pandas.testing import assert_frame_equal
from sklearn.pipeline import Pipeline
from .custom_estimators import ARIMAEstimator, ProphetEstimator

@pytest.fixture
def supply_pipelines() -> dict:
    """
    Provide a dictionary containing the cleaning and the preparation pipelines
    """
    cleaning_pipeline = Pipeline([
        ('remove_duplicates', RemoveDuplicates('Dates')),
        ('remove_errors', RemoveDateErrors('Dates'))
    ])

    preparation_pipeline = Pipeline([
        ('convert_to_datetime', ConvertToDatetime('Dates')),
        ('sort_by_index', SortByIndex('Dates')),
        ('set_frequency', SetFrequency('10min')),
        ('interpolation', Interpolation()),
        ('resampler', Resampler('H', 'Emissions')),
        ('boxcox', BoxCox('Emissions'))
    ])

    pipelines = {}
    pipelines['cleaning'] = cleaning_pipeline
    pipelines['preparation'] = preparation_pipeline

    return pipelines

def test_arima_estimator(supply_pipelines):
    """
    Test if the ARIMA estimator is capable of yield predictions
    """
    transformation_pipeline = Pipeline([
        ('cleaning', supply_pipelines['cleaning']),
        ('preparation', supply_pipelines['preparation'])
    ])

    original_df = pandas.DataFrame({
        'Dates': ['2020-01-01 01:00', '2020-01-01 01:10',
                '2020-01-01 01:10', '2020-01-01 01:20',
                '2020-01-01 01:20', '2020-01-01 01:30',
                '2020-01-01 01:40', '2020-01-01 01:50',
                '2020-01-01 2A:00', '2020-01-01 2A:10',
                '2020-01-01 2A:20', '2020-01-01 2A:30',
                '2020-01-01 2A:40', '2020-01-01 2A:50',
                '2020-01-01 2B:00', '2020-01-01 2B:10',
                '2020-01-01 03:00', '2020-01-01 03:10',
                '2020-01-01 03:20', '2020-01-01 03:30',
                '2020-01-01 03:40', '2020-01-01 03:50',
                '2020-01-01 04:00', '2020-01-01 04:10',
                '2020-01-01 04:20', '2020-01-01 04:30',
                '2020-01-01 04:40', '2020-01-01 04:50'],
        'Emissions': [2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5,
                    5, 5, 5, 8, 8, 2, 2, 2, 2, 2, 2, 5,
                    5, 5, 5, 5, 5]
    })
    
    # Creates the ARIMA estimator
    arima = ARIMAEstimator()

    pipeline = Pipeline([
        ('transformers', transformation_pipeline),
        ('estimator', ARIMAEstimator())
    ])

    # Prepares the data
    prepared_data = transformation_pipeline.fit_transform(original_df)

    # Trains the model
    arima.fit(prepared_data)
    
    # Generates predictions of 1 step in the future
    predictions = arima.predict(1)
    # Transforms the predicted values to its original scale
    predictions = transformation_pipeline['preparation']['boxcox'].inverse_transform(predictions)

    # Assert if the predictions values are a numpy array
    assert isinstance(predictions.values, numpy.ndarray)

def test_prophet_estimator(supply_pipelines):
    """
    Test if the Prophet estimator is capable of yield predictions
    """
    transformation_pipeline = Pipeline([
        ('cleaning', supply_pipelines['cleaning']),
        ('preparation', supply_pipelines['preparation'])
    ])

    original_df = pandas.DataFrame({
        'Dates': ['2020-01-01 01:00', '2020-01-01 01:10',
                '2020-01-01 01:10', '2020-01-01 01:20',
                '2020-01-01 01:20', '2020-01-01 01:30',
                '2020-01-01 01:40', '2020-01-01 01:50',
                '2020-01-01 2A:00', '2020-01-01 2A:10',
                '2020-01-01 2A:20', '2020-01-01 2A:30',
                '2020-01-01 2A:40', '2020-01-01 2A:50',
                '2020-01-01 2B:00', '2020-01-01 2B:10',
                '2020-01-01 03:00', '2020-01-01 03:10',
                '2020-01-01 03:20', '2020-01-01 03:30',
                '2020-01-01 03:40', '2020-01-01 03:50',
                '2020-01-01 04:00', '2020-01-01 04:10',
                '2020-01-01 04:20', '2020-01-01 04:30',
                '2020-01-01 04:40', '2020-01-01 04:50'],
        'Emissions': [2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5,
                    5, 5, 5, 8, 8, 2, 2, 2, 2, 2, 2, 5,
                    5, 5, 5, 5, 5]
    })
    
    # Creates the ARIMA estimator
    prophet = ProphetEstimator()

    # Prepares the data
    prepared_data = transformation_pipeline.fit_transform(original_df)

    # Trains the model
    prophet.fit(prepared_data)
    
    # Generates predictions of 1 step in the future
    predictions = prophet.predict(1)
    # Transforms the predicted values to its original scale
    predictions = transformation_pipeline['preparation']['boxcox'].inverse_transform(predictions)

    # Assert if the predictions values are a numpy array
    assert isinstance(predictions.values, numpy.ndarray)