from datetime import datetime


def calculate_time(func):
    def inner(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        stop = datetime.now()
        time_response = (stop - start)
        print(f'Заняло времени y {func.__name__}:', time_response)
        return result
    return inner
