from formating.formating_date import date_formation
from datetime import datetime

from time_comparison import calculate_time


@calculate_time
def rewrite_search(df) -> dict:
    """Поиск места разрыва (перезаписи) в файле: где стоят рядом самое большое значение и самое маленькое
       return: Словарь, с двумя индексами, между которых находится или остутствует разрыв 
    """
    min_index = 0
    max_index = len(df)-1
    while True:
        mid_index = (min_index + max_index) // 2
        # Точка выхода
        if max_index == min_index + 1:
            return {'min_index': min_index, 'max_index': max_index}

        if date_formation(df.loc[min_index]['Дата и время записи']) < date_formation(df.loc[mid_index]['Дата и время записи']):
            min_index = mid_index
        else:
            max_index = mid_index


@calculate_time
def searching_index(date: datetime, df) -> int | None:
    """Поиск индекса в отсортированном массиве, перед которым находится элемент date
       return: int, если индекс существует, None, если его нет 
    """
    if date <= date_formation(df.loc[0]['Дата и время записи']):
        return 0
    elif date > date_formation(df.iloc[-1]['Дата и время записи']):
        return None
    else:
        min_index = 0
        max_index = len(df)-1
        while True:
            mid_index = (min_index + max_index) // 2
            guess = date_formation(df.loc[mid_index]['Дата и время записи'])
            if date_formation(df.loc[mid_index-1]['Дата и время записи']) < date <= guess:
                return mid_index
            elif guess > date:
                max_index = mid_index - 1
            else:
                min_index = mid_index + 1
