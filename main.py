import os
import csv
import pandas as pd
from pathlib import Path
from formating.formating_date import date_formation
from formating.formating_dataframe import dataframe_formation
from algorithms import rewrite_search, searching_index
from time_comparison import calculate_time

PARENT_DIR = Path(__file__).resolve().parent

# data_path = os.path.join(PARENT_DIR, 'csv_data/data.csv')
data_path = os.path.join(PARENT_DIR, 'csv_data/УжатыйЦСВ.csv')
# data_path = os.path.join(PARENT_DIR, 'csv_data/new.csv')
# data_path = os.path.join(PARENT_DIR, 'csv_data/new_copy.csv')

df = pd.read_csv(filepath_or_buffer=data_path,
                 encoding='windows-1251')


# берет столбцы индекс и время из таблицы для всех строк
# df_data_to_find_start = df.loc[:, ['RecordID', 'Дата и время записи']]
# df_data = df.loc[:, ['RecordID', 'Дата и время записи']]


date_from = '18 августа 2022 г. 7:58:30.003 мсек'
date_to = '18 августа 2022 г. 9:21:50.028 мсек'
# date_to = '18 августа 2022 г. 7:58:41.028 мсек'


@calculate_time
def getting_range(date_from, date_to):

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


# это работает быстрее
@calculate_time
def writing_to_csv_by_aperture(df: pd.DataFrame, aperture) -> bool:
    """Запись строк в файл response.csv, у которых значение параметра отличается от предыдущей строки на значение, большее апертуры"""
    with open('csv_data/response.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(df.columns[1:])
        for i in range(0, len(df)-1):
            previous = df.iloc[i]
            next = df.iloc[i+1]
            if abs(next[aperture['parametr']] - previous[aperture['parametr']]) > aperture['value']:
                writer.writerow(next)
    return True


# это работает
# @calculate_time
# def writing_to_csv_by_aperture(df: pd.DataFrame, aperture) -> bool:
#     """Запись строк в файл response.csv, у которых значение параметра отличается от предыдущей строки на значение, большее апертуры"""
#     with open('csv_data/response.csv', 'w') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',')
#         writer.writerow(df.columns[1:])
#         for i in range(0, len(df)-1):
#             previous = df.iloc[i]
#             next = df.iloc[i+1]
#             if abs(next[aperture['parametr']] - previous[aperture['parametr']]) > aperture['value']:
#                 writer.writerow(next[1:])
#     return True


# это работает быстрее
@calculate_time
def main(date_from, date_to, aperture: dict = {'parametr': 'п2673', 'value': 10}):
    sorted_dataframe = pd.concat(
        [getting_range(date_from, date_to)], ignore_index=True)
    writing_to_csv_by_aperture(sorted_dataframe, aperture)
    return 'Done'

# это работает
# @calculate_time
# def main(date_from, date_to, aperture: dict = {'parametr': 'п2673', 'value': 10}):
#     sorted_dataframe = getting_range(date_from, date_to).reset_index()
#     writing_to_csv_by_aperture(sorted_dataframe, aperture)
#     return 'Done'


print(main(date_from, date_to))
