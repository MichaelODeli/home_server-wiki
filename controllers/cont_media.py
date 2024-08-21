import time

def getDuration(seconds_data):
    """
    Преобразует количество секунд в формат времени HH:MM:SS.

    Параметры:
    seconds_data (float): Количество секунд.

    Вывод:
    str: Строка в формате HH:MM:SS, представляющая время.
    """
    if seconds_data < 3600:
        time_format = "%M:%S"
    else:
        time_format = "%H:%M:%S"
    return time.strftime(time_format, time.gmtime(float(seconds_data)))