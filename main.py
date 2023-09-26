import os
import csv
import pandas as pd
from pathlib import Path
from formating.formating_date import date_formation
from formating.formating_dataframe import dataframe_formation
from algorithms import rewrite_search, searching_index
from time_comparison import calculate_time

PARENT_DIR = Path(__file__).resolve().parent

# Путь до исходного файла с данными .csv
data_path = os.path.join(PARENT_DIR, 'csv_data/data.csv')

# Чтение файла
df = pd.read_csv(filepath_or_buffer=data_path, encoding='windows-1251')

# Дефолтные значения даты и времени для выборки
date_from = '18 августа 2022 г. 0:50:30.003 мсек'
date_to = '18 августа 2022 г. 8:21:50.028 мсек'
# date_to = '18 августа 2022 г. 7:58:41.028 мсек'


@calculate_time
def getting_range(date_from=date_from, date_to=date_to) -> pd.DataFrame:
    """Выборка всего временного промежутка, начиная с date_from, заканчивая date_to в датафрейме"""
    formated_date_from = date_formation(date_from)
    formated_date_to = date_formation(date_to)
    indexex_of_break = rewrite_search(df)
    # Сравнение элементов. Если дата элемента с меньшим индексом больше даты элемента с большим: был разрыв и нужна сортировка
    if date_formation(df.loc[indexex_of_break['min_index']]['Дата и время записи']) > \
            date_formation(df.loc[indexex_of_break['max_index']]['Дата и время записи']):
        sorted_df = dataframe_formation(indexex_of_break['max_index'], df)
    else:
        sorted_df = df

    index_from = searching_index(formated_date_from, sorted_df)
    index_to = searching_index(formated_date_to, sorted_df)

    if index_from == None or index_to == 0:
        print('Нет такого временного диапазона')
        return
    elif index_to == None:
        response = sorted_df[index_from:]
    else:
        response = sorted_df[index_from:index_to+1]

    return response


@calculate_time
def writing_to_csv_by_aperture(df: pd.DataFrame, aperture) -> bool:
    """Запись строк в файл response.csv, у которых значение параметра отличается от предыдущей строки на значение, большее апертуры
       Значения записываются в файл csv_data/response.csv
    """
    with open('csv_data/response.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(df.columns[1:])
        for i in range(0, len(df)-1):
            previous = df.iloc[i]
            next = df.iloc[i+1]
            if abs(next[aperture['parametr']] - previous[aperture['parametr']]) > aperture['value']:
                writer.writerow(next)
    return True


@calculate_time
def main(date_from=date_from, date_to=date_to, aperture: dict = {'parametr': 'п2673', 'value': 10}):
    """Основная исполняемая функция, объединяет функцию выборки на основе вводимых дат, функцию выборки на основе вводимого параметра и записи в .csv"""
    sorted_dataframe = pd.concat(
        [getting_range(date_from, date_to)], ignore_index=True)
    writing_to_csv_by_aperture(sorted_dataframe, aperture)
    return 'Done'


print(main())
