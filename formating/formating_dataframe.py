import pandas as pd


def dataframe_formation(index, df):
    return pd.concat([df[index:], df[:index]], ignore_index=True)
