import requests
from dash import (
    dcc,
    html,
)
import dash_mantine_components as dmc
from controllers.cont_torrents import bytes2human
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import calendar
import shutil
import psutil
from dash_iconify import DashIconify

import locale
locale.setlocale(locale.LC_ALL, "ru_RU")


def get_torrent_status(BASE_URL):
    """
    Получает статус торрентов из qBittorrent API.

    Параметры:
    BASE_URL (str): Базовый URL для доступа к qBittorrent API.

    Вывод:
    tuple: Кортеж с тремя строками, представляющими информацию о статусе торрентов.
           Первая строка - количество активных торрентов.
           Вторая строка - количество торрентов, скачиваемых в данный момент.
           Третья строка - количество торрентов, которые раздаются.

    Примечание:
    Если возникает ошибка при получении данных от qBittorrent API,
    возвращается кортеж с тремя строками, содержащими сообщение "qbittorrent не отвечает.".
    """
    try:
        response = requests.get(f"{BASE_URL}/api/v2/auth/login", timeout=10)
        # print(response.json())
        if response.status_code == 200:
            count_all = len(
                requests.get(f"{BASE_URL}/api/v2/torrents/info").json()
            )  # всего
            count_downloading = len(
                requests.get(f"{BASE_URL}/api/v2/torrents/info?filter=downloading").json()
            )  # скачивается
            count_down_av = len(
                requests.get(
                    f"{BASE_URL}/api/v2/torrents/info?filter=stalled_downloading"
                ).json()
            )  # доступны к раздаче
            count_active = len(
                requests.get(f"{BASE_URL}/api/v2/torrents/info?filter=active").json()
            )  # активны
            count_completed = len(
                requests.get(f"{BASE_URL}/api/v2/torrents/info?filter=completed").json()
            )  # активны

            count_upl = count_active - count_downloading  # раздаются
            return (
                f"Активных: {count_all}",
                f"Скачивается: {count_downloading}",
                f"Раздается: {count_upl}",
            )
        else:
            raise ConnectionError
    except:
        return ['qbittorrent не отвечает.']*3


def get_progress(
    drive: str, current_value: float, max_value: float, id: str, valid: bool
):
    """
    Получить прогресс-бар с текущим объемом накопителя

    Параметры:
    - drive: название диска/раздела
    - current_value: текущий занятый объем диска
    - max_value: максимальная емкость раздела
    - id: идентификатор блока
    - valid: "существование" раздела. Если нет - то прогресс-бар будет окрашен в красный цвет.

    """
    percent = int(round(current_value / max_value, 2) * 100)
    if valid == True:
        return html.Tr(
            [
                html.Td(drive),
                html.Td(
                    dmc.ProgressRoot(
                        [
                            dmc.ProgressSection(
                                dmc.ProgressLabel(drive),
                                value=percent,
                                color="cyan",
                            )
                        ],
                        size="xl",
                    ),
                    style={"width": "100%", "padding": "0 2% 0 2%"},
                ),
            ]
        )
    else:
        return html.Tr(
            [
                html.Td(drive),
                html.Td(
                    dmc.ProgressRoot(
                        [
                            dmc.ProgressSection(
                                dmc.ProgressLabel("Диск не обнаружен"),
                                value=100,
                                color="#cc0000",
                                id=id
                            )
                        ],
                        size="xl",
                    ),
                    style={"width": "100%", "padding": "3%"},
                ),
            ]
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

    return get_progress(
        partition, int(used), int(total), f"ring-{partition}", valid=valid
    )


def widget_disk_size(**kwargs):
    """
    Функция создает карточку с информацией о свободном месте на дисках.

    Аргументы:
    **kwargs: любое количество ключевых аргументов.

    Возвращает:
    dbc.Card: карточка с информацией о свободном месте на дисках.
    """
    return dbc.Card(
        [
            html.H5(
                "Свободное место на дисках",
                style={"text-align": "center"},
                className="card-title",
            ),
            dmc.Space(h=10),
            html.Table(
                [
                    get_drive_size("/mnt/sdb1/"),
                    get_drive_size("/mnt/sdc1/"),
                    get_drive_size("/mnt/sdd1/"),
                ]
            ),
            dmc.Space(h=10),
            html.A("Подробные свойства", href='/settings?l=y&tab=server_info'),

        ],
        className="block-background mobile-block",
        # style={"min-height": "100%"},
    )


def get_weather_label(selected_date: str, temperature: list, weather_type="sunny"):
    """
    Функция создает метку с информацией о погоде.

    Аргументы:
    selected_date (str): дата в формате DDMMYYYY.
    temperature (list): список с температурой в формате [day_temp, night_temp].
    weather_type (str): тип погоды, по умолчанию "sunny".

    Возвращает:
    dmc.Stack: метка с информацией о погоде.
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
                c="var(--bs-blue)" if converted_date.weekday() < 5 else "red",
            ),
            dmc.Text(
                f"{converted_date.day} {calendar.month_abbr[converted_date.month]}",
                c="var(--bs-gray)",
            ),
            dmc.Space(h=10),
            DashIconify(icon=weather_types[weather_type], width=40),
            dmc.Text(temperature[0], c="var(--bs-blue)"),
            dmc.Text(temperature[1], c="var(--bs-gray)"),
        ],
        align="center",
        gap=0,
    )


def get_date_str(plus=0, pattern="%d%m%Y"):
    """
    Вывод сегодняшней даты с опцией добавление определенного числа дней к числу.

    Паттерн по умолчанию - DDMMYYYY

    """
    today = datetime.today()
    needed_date = today + timedelta(days=plus) if plus > 0 else today
    return needed_date.strftime(pattern)


def widget_weather(**kwargs):
    """
    Функция создает карточку с информацией о погоде.

    Аргументы:
    **kwargs: любое количество ключевых аргументов.

    Возвращает:
    dbc.Card: карточка с информацией о погоде.
    """
    return dbc.Card(
        [
            html.H5(
                "Погода в г. Среднеуральск",
                style={"text-align": "center"},
                className="card-title",
            ),
            dmc.Space(h=5),
            dmc.Group(
                [
                    get_weather_label(get_date_str(0), ["+1", "-4"], "cloudy"),
                    get_weather_label(get_date_str(1), ["+10", "-4"], "sunny"),
                    get_weather_label(get_date_str(2), ["+1", "-4"], "partly-cloudy"),
                    get_weather_label(get_date_str(3), ["+10", "-4"], "thunderstorm"),
                    get_weather_label(get_date_str(4), ["+1", "-40"], "rain"),
                ],
                justify="center",
                gap="xs",
                # style={'display': 'inline-flex', 'flex-direction': 'column'}
            ),
        ],
        className="block-background mobile-block",
        # style={"min-height": "100%"},
    )


def widget_torrents(qbittorrent_url):
    """
    Функция создает карточку с информацией о торрентах.

    Аргументы:
    qbittorrent_url (str): URL-адрес qbittorrent.

    Возвращает:
    dbc.Card: карточка с информацией о торрентах.
    """
    return dbc.Card(
        [
            html.H5("Мониторинг торрентов", className="card-title"),
            dmc.Space(h=10),
            dmc.Stack(
                [
                    dmc.Text("Активных: NaN", id="home-torrents-active"),
                    dmc.Text("Скачивается: NaN", id="home-torrents-download"),
                    dmc.Text("Раздается: NaN", id="home-torrents-upload"),
                ],
                style={"text-align": "left"},
                gap="xs",
            ),
            dmc.Space(h=15),
            html.A("Открыть qbittorrent", href=qbittorrent_url),
        ],
        className="block-background mobile-block",
        # style={"min-height": "100%"},
    )


def widget_systeminfo():
    """
    Функция создает карточку с информацией о системе.

    Аргументы:
    Нет аргументов.

    Возвращает:
    dbc.Card: карточка с информацией о системе.
    """
    return dbc.Card(
        [
            html.H5("Системный монитор", className="card-title"),
            dmc.Space(h=10),
            dmc.Group(
                [
                    dmc.Stack(
                        [
                            dmc.Text("CPU", ta="center", fw=700),
                            dmc.RingProgress(
                                sections=[
                                    {
                                        "value": int(psutil.cpu_percent()),
                                        "color": "var(--bs-blue)",
                                        "tooltip": f"Используется: {psutil.cpu_percent()}%",
                                    },
                                ],
                                label=dmc.Text(f"{round(psutil.cpu_freq().current/1000, 2)} GHz", c="black", ta="center"),
                                size=120,
                                roundCaps=True,
                            ),
                        ],
                        gap=0,
                    ),
                    dmc.Stack(
                        [
                            dmc.Text("RAM", ta="center", fw=700),
                            dmc.RingProgress(
                                sections=[
                                    {
                                        "value": psutil.virtual_memory().percent,
                                        "color": "var(--bs-blue)",
                                        "tooltip": f"Занято: {bytes2human(psutil.virtual_memory().used)}",
                                    },
                                ],
                                label=dmc.Text(bytes2human(psutil.virtual_memory().total), c="black", ta="center"),
                                size=120,
                                roundCaps=True,
                            ),
                        ],
                        gap=0,
                    ),
                    dmc.Stack(
                        [
                            dmc.Text("SWAP", ta="center", fw=700),
                            dmc.RingProgress(
                                sections=[
                                    {
                                        "value": psutil.swap_memory().percent,
                                        "color": "var(--bs-blue)",
                                        "tooltip": f"Занято: {bytes2human(psutil.swap_memory().used)}",
                                    },
                                ],
                                label=dmc.Text(bytes2human(psutil.swap_memory().total), c="black", ta="center"),
                                size=120,
                                roundCaps=True,
                            ),
                        ],
                        gap=0,
                    ),
                ],
            ),
            dmc.Divider(h=10),
            dmc.Grid(
                [
                    dmc.GridCol(
                        dmc.Group(
                            [
                                dmc.Text("↓", fw=600, c="#369e1f"),
                                dmc.Text("0 b/s", c="#369e1f"),
                            ],
                            justify="center",
                        ),
                        span="content",
                    ),
                    dmc.GridCol(
                        dmc.Group(
                            [
                                dmc.Text("↑", fw=600, c="blue"),
                                dmc.Text("0 b/s", c="blue"),
                            ],
                            justify="center",
                        ),
                        span="content",
                    ),
                ],
                w="100%",
                grow=True,
            ),
        ],
        className="block-background mobile-block",
        style={"min-height": "100%", "width": "100%"},
    )


def widget_fileManager_log():
    # статистика по добавленным файлам
    return None
