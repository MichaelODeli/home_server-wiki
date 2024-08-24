import requests
from dash import (
    dcc,
    html,
)
import dash_mantine_components as dmc
from controllers.cont_torrents import bytes2human
from controllers import db_connection, cont_torrents, file_manager
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import calendar
import shutil
import psutil
from dash_iconify import DashIconify

import locale

locale.setlocale(locale.LC_ALL, "ru_RU")


def getTorrentStatus():
    """
    Получает статус торрентов из qBittorrent API.
    """
    try:
        torrents_dict = cont_torrents.getTorrentsDataDict(source_page="main_page")

        count_all = torrents_dict["all"]
        count_downloading = torrents_dict["downloading"]
        count_uploading = torrents_dict["uploading"]

        return (
            f"Активных: {count_all}",
            f"Скачивается: {count_downloading}",
            f"Раздается: {count_uploading}",
        )
    except:
        return ["qbittorrent не отвечает."] * 3


def getColorByValue(current_value=None, max_value=None, percent=None):
    if percent == None:
        percent = (current_value / max_value) * 100
    return (
        "var(--bs-primary)" if percent < 70 else ("orange" if percent < 90 else "red")
    )


def getProgress(
    drive: str,
    current_value: float,
    max_value: float,
    id: str,
    valid: bool,
    readable=None,
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

    if valid == True:
        return html.Tr(
            [
                html.Td(drive),
                html.Td(
                    dmc.ProgressRoot(
                        [
                            dmc.ProgressSection(
                                dmc.ProgressLabel(
                                    f"{bytes2human(current_value)} | {bytes2human(max_value)}"
                                ),
                                value=int(round(current_value / max_value, 2) * 100),
                                color=getColorByValue(current_value, max_value),
                                id=id,
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
                                id=id,
                            )
                        ],
                        size="xl",
                    ),
                    style={"width": "100%", "padding": "3%"},
                ),
            ]
        )


def getDriveSize(partition):
    """
    Получить размер диска/раздела в виде кольцевого прогресс-бара.

    Параметры:
    - partition: путь к разделу
    """
    try:
        mountpoint = partition.mountpoint
        total, used, _ = shutil.disk_usage(mountpoint)
        valid = True
    except Exception:
        total = 1
        used = 1
        valid = False

    return getProgress(
        mountpoint, int(used), int(total), f"ring-{mountpoint}", valid=valid
    )


def widgetDiskSize(**kwargs):
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
                "Свободное место на разделах",
                style={"text-align": "center"},
                className="card-title",
            ),
            dmc.Space(h=10),
            html.Table([getDriveSize(part) for part in psutil.disk_partitions()]),
            dmc.Space(h=10),
            html.A("Подробные свойства", href="/settings?l=y&tab=server_info"),
        ],
        className="block-background mobile-block",
        # style={"min-height": "100%"},
    )


def getWeatherLabel(selected_date: str, temperature: list, weather_type="sunny"):
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


def getDateString(plus=0, pattern="%d%m%Y"):
    """
    Вывод сегодняшней даты с опцией добавление определенного числа дней к числу.

    Паттерн по умолчанию - DDMMYYYY

    """
    today = datetime.today()
    needed_date = today + timedelta(days=plus) if plus > 0 else today
    return needed_date.strftime(pattern)


def widgetWeather(**kwargs):
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
                    getWeatherLabel(getDateString(0), ["+1", "-4"], "cloudy"),
                    getWeatherLabel(getDateString(1), ["+10", "-4"], "sunny"),
                    getWeatherLabel(getDateString(2), ["+1", "-4"], "partly-cloudy"),
                    getWeatherLabel(getDateString(3), ["+10", "-4"], "thunderstorm"),
                    getWeatherLabel(getDateString(4), ["+1", "-40"], "rain"),
                ],
                justify="center",
                gap="xs",
                # style={'display': 'inline-flex', 'flex-direction': 'column'}
            ),
        ],
        className="block-background mobile-block",
        # style={"min-height": "100%"},
    )


def widgetTorrents():
    """
    Функция создает карточку с информацией о торрентах.
    """
    conn = db_connection.getConn()
    settings = file_manager.getSettings(conn)

    qbt_ip = settings["apps.torrents.qbittorrent_ip"]
    qbt_port = settings["apps.torrents.qbittorrent_port"]

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
            html.A(
                "Открыть qbittorrent",
                href="http://" + qbt_ip + ":" + qbt_port,
                target="_blank",
            ),
            dmc.LoadingOverlay(
                visible=False,
                id="loading-overlay-widget-torrent",
                zIndex=1000,
                overlayProps={"radius": "sm", "blur": 2},
            ),
        ],
        className="block-background mobile-block",
        # style={"min-height": "100%"},
    )


def widgetSysteminfo():
    """
    Функция создает карточку с информацией о системе.

    Аргументы:
    Нет аргументов.

    Возвращает:
    dbc.Card: карточка с информацией о системе.
    """

    cpu_usage = int(psutil.cpu_percent(interval=0.1))
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
                                        "value": cpu_usage,
                                        "color": getColorByValue(percent=cpu_usage),
                                        "tooltip": f"Используется: {cpu_usage}%",
                                    },
                                ],
                                label=dmc.Text(
                                    f"{round(psutil.cpu_freq().current/1000, 2)} GHz",
                                    c="var(--bs-body-color)",
                                    ta="center",
                                ),
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
                                        "color": getColorByValue(
                                            percent=psutil.virtual_memory().percent
                                        ),
                                        "tooltip": f"Занято: {bytes2human(psutil.virtual_memory().used)}",
                                    },
                                ],
                                label=dmc.Text(
                                    bytes2human(psutil.virtual_memory().total),
                                    c="var(--bs-body-color)",
                                    ta="center",
                                ),
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
                                        "color": getColorByValue(
                                            percent=psutil.swap_memory().percent
                                        ),
                                        "tooltip": f"Занято: {bytes2human(psutil.swap_memory().used)}",
                                    },
                                ],
                                label=dmc.Text(
                                    bytes2human(psutil.swap_memory().total),
                                    c="var(--bs-body-color)",
                                    ta="center",
                                ),
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
                                dmc.Text("↓", fw=600),
                                dmc.Text("NaN b/s"),
                            ],
                            justify="center",
                            c="#369e1f",
                        ),
                        span="content",
                    ),
                    dmc.GridCol(
                        dmc.Group(
                            [
                                dmc.Text("↑", fw=600),
                                dmc.Text("NaN b/s"),
                            ],
                            justify="center",
                            c="blue",
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


def widgetFileManagerLog():
    # статистика по добавленным файлам
    return None


def getHeaderLinks(conn):
    with conn.cursor() as cursor:
        cursor.execute("select * from header_links;")
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data
