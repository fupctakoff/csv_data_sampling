from datetime import datetime

DATA_FOR_MONTHS = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
}


def date_formation(elem) -> datetime:
    """Форматирование элементов в формат datetime для удобного сравнения"""
    elems_ymd = elem[:-20].split(' ')  # день месяц год
    elems_hmsm = elem[-17:-5].split(':')  # час минута секунда милисекунда
    elems_datetime = datetime(year=int(elems_ymd[2]), month=DATA_FOR_MONTHS[elems_ymd[1]], day=int(elems_ymd[0]), hour=int(elems_hmsm[0]),
                              minute=int(elems_hmsm[1]), second=int(elems_hmsm[2][:2]), microsecond=int(elems_hmsm[2][-3:]))
    return elems_datetime
