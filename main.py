import os
import pandas as pd
from pathlib import Path
from formating.formating_date import date_formation
from formating.formating_dataframe import dataframe_formation
from algorithms import rewrite_search, searching_index
from time_comparison import calculate_time

PARENT_DIR = Path(__file__).resolve().parent

# data_path = os.path.join(PARENT_DIR, 'csv_data/data.csv')
# data_path = os.path.join(PARENT_DIR, 'csv_data/УжатыйЦСВ.csv')
# data_path = os.path.join(PARENT_DIR, 'csv_data/new.csv')
data_path = os.path.join(PARENT_DIR, 'csv_data/new_copy.csv')

df = pd.read_csv(filepath_or_buffer=data_path, encoding='windows-1251')

# берет столбцы индекс и время из таблицы для всех строк
df_data_to_find_start = df.loc[:, ['RecordID', 'Дата и время записи']]
df_data = df.loc[:, ['RecordID', 'Дата и время записи']]


date_from = '18 августа 2022 г. 7:58:30.003 мсек'
# date_to = '18 августа 2022 г. 9:21:50.028 мсек'
date_to = '18 августа 2022 г. 7:58:41.028 мсек'

@calculate_time
def main(date_from, date_to):

    formated_date_from = date_formation(date_from)
    formated_date_to = date_formation(date_to)
    indexex_of_break = rewrite_search(df_data)

    # Сравнение элементов. Если дата элемента с меньшим индексом больше даты элемента с большим: был разрыв и нужна сортировка
    if date_formation(df_data.loc[indexex_of_break['min_index']]['Дата и время записи']) > \
            date_formation(df_data.loc[indexex_of_break['max_index']]['Дата и время записи']):
        sorted_df = dataframe_formation(indexex_of_break['max_index'], df_data)
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

    print('Выборка для вводимых дат:\n', response)


main(date_from, date_to)
