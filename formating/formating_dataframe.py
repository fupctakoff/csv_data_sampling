import pandas as pd

from time_comparison import calculate_time


@calculate_time
def dataframe_formation(index, df):
    return pd.concat([df[index:], df[:index]], ignore_index=True)
