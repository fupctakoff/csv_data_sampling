import pandas as pd


def dataframe_formation(index: int, df: pd.DataFrame) -> pd.DataFrame:
    """Отрезает датафрейм по индексу, и вставляет конец в начало"""
    return pd.concat([df[index:], df[:index]], ignore_index=True)
