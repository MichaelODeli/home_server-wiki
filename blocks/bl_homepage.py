from dash import (
    dcc,
    html,
)
import dash_mantine_components as dmc
from datetime import datetime, timedelta
import calendar
import shutil
from dash_iconify import DashIconify

import locale
locale.setlocale(locale.LC_ALL, "ru_RU")


def get_ring(drive: str, current_value: float, max_value: float, id: str, valid: bool):
    """
    Получить кольцевой прогресс-бар с текущим размерос накопителя

    Параметры:
    - drive: название диска/раздела
    - current_value: текущий занятый объем диска
    - max_value: максимальная емкость раздела
    - id: идентификатор блока
    - valid: "существование" раздела. Если нет - то прогресс-бар будет окрашен в красный цвет.

    """
    percent = int(round(current_value / max_value, 2) * 100)
    if valid == True:
        return dmc.Stack(
            [
                dmc.RingProgress(
                    id=id,
                    sections=[{"value": percent, "color": "--bs-primary"}],
                    label=dmc.Center(
                        dmc.Text(f"{str(percent)}%", color="--bs-primary", size=20)
                    ),
                    roundCaps=True,
                    size=100,
                ),
                dmc.Text(f"{drive}: {current_value} GB / {max_value} GB"),
            ],
            spacing=0,
            align="center",
        )
    else:
        return dmc.Stack(
            [
                dmc.RingProgress(
                    id=id,
                    sections=[{"value": 100, "color": "var(--bs-danger)"}],
                    label=dmc.Center(dmc.Text("NaN", color="--bs-primary", size=20)),
                    roundCaps=True,
                    size=100,
                ),
                dcc.Markdown(
                    f"""
                    Раздел *{drive}*   
                    не обнаружен"""
                ),
            ],
            spacing=0,
            align="center",
        )


def get_drive_size(partition):
    """
    Получить размер диска/раздела в виде кольцевого прогресс-бара.

    Параметры:
    - partition: путь к разделу
    """
    try:
        total, used, _ = shutil.disk_usage(partition)

        total = total // (2**30)
        used = used // (2**30)
        valid = True
    except FileNotFoundError:
        total = 1
        used = 1
        valid = False

    return get_ring(partition, int(used), int(total), f"ring-{partition}", valid=valid)


def widget_disk_size(**kwargs):
    return html.Div(
        [
            html.H5("Свободное место на дисках", style={"text-align": "center"}),
            dmc.Group(
                [
                    get_drive_size("/mnt/sdb1/"),
                    get_drive_size("/mnt/sdc1/"),
                    get_drive_size("/mnt/sdd1/"),
                ],
                position="center",
                spacing="xs",
            ),
        ],
        className="block-background mobile-block",
    )


def get_weather_label(selected_date: str, temperature: list, weather_type="sunny"):
    """
    - selected_date - DDMMYYYY str
    - temperature - list [day_temp, night_temp]
    """
    weather_types = {
        "sunny": "material-symbols:sunny",
        "partly-cloudy": "material-symbols:partly-cloudy-day",
        "cloudy": "material-symbols:cloudy",
        "snow": "material-symbols:cloudy-snowing",
        "rain": "material-symbols:rainy",
        "thunderstorm": "material-symbols:thunderstorm",
    }
    if weather_type not in weather_types:
        raise ValueError("Incorrect weather type.")

    converted_date = datetime.strptime(selected_date, "%d%m%Y").date()
    return dmc.Stack(
        [
            dmc.Text(
                calendar.day_abbr[converted_date.weekday()].capitalize(),
                color="var(--bs-blue)" if converted_date.weekday() < 5 else "red",
            ),
            dmc.Text(
                f"{converted_date.day} {calendar.month_abbr[converted_date.month]}",
                color="var(--bs-gray)",
            ),
            dmc.Space(h=10),
            DashIconify(icon=weather_types[weather_type], width=40),
            dmc.Text(temperature[0], color="var(--bs-blue)"),
            dmc.Text(temperature[1], color="var(--bs-gray)"),
        ],
        align="center",
        spacing=0,
    )


def get_date_str(plus=0, pattern='%d%m%Y'):
    """
    Вывод сегодняшней даты с опцией добавление определенного числа дней к числу. 

    Паттерн по умолчанию - DDMMYYYY
    
    """
    today = datetime.today()
    needed_date = today + timedelta(days=plus) if plus > 0 else today
    return needed_date.strftime(pattern)


def widget_weather(**kwargs):
    "Виджет с информацией о погоде"
    return html.Div(
        [
            html.H5("Погода в г. Среднеуральск", style={"text-align": "center"}),
            dmc.Space(h=5),
            dmc.Group(
                [
                    get_weather_label(get_date_str(0), ["+1", "-4"], "cloudy"),
                    get_weather_label(get_date_str(1), ["+10", "-4"], "sunny"),
                    get_weather_label(get_date_str(2), ["+1", "-4"], "partly-cloudy"),
                    get_weather_label(get_date_str(3), ["+10", "-4"], "thunderstorm"),
                    get_weather_label(get_date_str(4), ["+1", "-40"], "rain"),
                ],
                position="center",
                spacing="xs",
                # style={'display': 'inline-flex', 'flex-direction': 'column'}
            ),
        ],
        className="block-background mobile-block",
    )


def widget_torrents(qbittorrent_url):
    """Виджет с информацией о торрентах"""
    return html.Div(
        [
            html.H5("Информация по торрентам"),
            dmc.Space(h=5),
            dmc.Stack(
                [
                    dmc.Text("Активных торрентов: NaN", id="home-torrents-active"),
                    dmc.Text("Скачивается: NaN", id="home-torrents-download"),
                    dmc.Text("Раздается: NaN", id="home-torrents-upload"),
                ],
                style={"margin": "auto"},
                spacing="xs",
            ),
            dmc.Space(h=15),
            html.A("Перейти в qbittorrent", href=qbittorrent_url),
        ],
        className="block-background mobile-block",
    )


def widget_system_usage():
    # не график, просто текущие значения
    return None


def widget_fileManager_log():
    # статистика по добавленным файлам
    return None