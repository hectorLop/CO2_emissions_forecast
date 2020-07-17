from __future__ import annotations
from sklearn.base import TransformerMixin
import pandas

class ConvertToDatetime(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> ConvertToDatetime:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

class SortByIndex(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> SortByIndex:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

class SetFrequency(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> SetFrequency:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

class Interpolation(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> Interpolation:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

class Resampler(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> Resampler:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass

class BoxCox(TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X: pandas.DataFrame, y=None) -> BoxCox:
        pass

    def transform(self, X: pandas.DataFrame) -> pandas.DataFrame:
        pass