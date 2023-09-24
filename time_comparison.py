from datetime import datetime


def calculate_time(func):
    def inner(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        stop = datetime.now()
        time_response = (stop - start)
        print('Заняло времени:', time_response)
        return result
    return inner
