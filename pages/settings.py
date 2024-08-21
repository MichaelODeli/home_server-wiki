from dash import (
    dcc,
    html,
    Input,
    Output,
    callback,
    register_page,
    State,
    Input,
    Output,
    no_update,
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_extensions import Purify
from flask import request
from datetime import datetime
from controllers import service_controller as service
from controllers import db_connection, file_manager
import psutil
import platform

register_page(__name__, path="/settings", icon="fa-solid:home")


def generateTableRow(param_name, param_value="", head=False):
    return html.Tr(
        [
            (
                html.Td(
                    param_name,
                    className="min-column-width",
                    style={"padding": "0.3rem" if param_value != "" else "1rem"},
                )
                if not head
                else html.Th(param_name, className="min-column-width")
            ),
            (
                html.Td(
                    param_value,
                    style={"padding": "0.3rem" if param_value != "" else "1rem"},
                )
                if not head
                else html.Th(param_value)
            ),
        ]
    )


def getSize(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def getSystemInfoRows():
    uname = platform.uname()
    return [
        generateTableRow(html.H6("Информация о системе")),
        generateTableRow("Операционная система", f"{uname.system}"),
        generateTableRow("Идентификатор устройства", f"{uname.node}"),
        generateTableRow("Релиз", f"{uname.release}"),
        generateTableRow("Версия ОС", f"{uname.version}"),
        generateTableRow("Архитектура", f"{uname.machine}"),
        generateTableRow("Процессор", f"{uname.processor}"),
    ]


def getCPUInfoRows():
    cpufreq = psutil.cpu_freq()
    return [
        generateTableRow(html.H6("Информация о процессоре")),
        generateTableRow(
            "Физических/логических ядер",
            f"{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}",
        ),
        generateTableRow(
            "Базовая частота",
            f"{cpufreq.current:.2f}Mhz",
        ),
        generateTableRow(
            "Использование ядер процессора",
            html.Div(
                [
                    dbc.Button(
                        "Показать",
                        id="show-cpu-load",
                    )
                ],
                id="cpu-ring-usage",
            ),
        ),
        generateTableRow(
            "Использование процессора",
            f"{psutil.cpu_percent()}%",
        ),
    ]


def getRAMSWARInfoRows():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return [
        generateTableRow(html.H6("ОЗУ")),
        generateTableRow("Всего", f"{getSize(svmem.total)}"),
        generateTableRow(
            "Доступно",
            f"{getSize(svmem.available)}",
        ),
        generateTableRow("Использовано", f"{getSize(svmem.used)}"),
        generateTableRow("Процент использования", f"{svmem.percent}%"),
        generateTableRow(html.H6("SWAP")),
        generateTableRow("Всего", f"{getSize(swap.total)}"),
        generateTableRow("Свободно", f"{getSize(swap.free)}"),
        generateTableRow("Использовано", f"{getSize(swap.used)}"),
        generateTableRow("Процент использования", f"{swap.percent}%"),
    ]


def getPartitionsInfoRows():
    partitions = psutil.disk_partitions()
    parts_data = []
    for partition in partitions:
        partition_data = []
        partition_data.append(dcc.Markdown(f"**Устройство**: {partition.device}"))
        partition_data.append(
            dcc.Markdown(f"**Точка монтирования**: {partition.mountpoint}")
        )
        partition_data.append(dcc.Markdown(f"**Файловая система**: {partition.fstype}"))
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            partition_data.append(
                dcc.Markdown(f"**Всего доступно**: {getSize(partition_usage.total)}")
            )
            partition_data.append(
                dcc.Markdown(f"**Использовано**: {getSize(partition_usage.used)}")
            )
            partition_data.append(
                dcc.Markdown(f"**Свободно**: {getSize(partition_usage.free)}")
            )
            partition_data.append(
                dcc.Markdown(f"**Процент использования**: {partition_usage.percent}%")
            )
        except PermissionError:
            continue
        parts_data.append(
            generateTableRow(partition.device, dmc.Stack(partition_data, gap="xs"))
        )

    return [generateTableRow(html.H6("Накопители и разделы"))] + parts_data


def layout(l="n", tab="server_info", **kwargs):
    if l == "n":
        return dmc.Container()
    service.logPrinter(request.remote_addr, "settings", "page opened")

    return dmc.Container(
        children=[
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab(html.H6("Основные настройки"), value="main"),
                            dmc.TabsTab(html.H6("Менеджер файлов"), value="files"),
                            dmc.TabsTab(
                                html.H6("Настройка виджетов и приложений"),
                                value="widgets",
                            ),
                            dmc.TabsTab(
                                html.H6("Свойства системы"), value="server_info"
                            ),
                        ],
                        grow=True,
                    ),
                ],
                variant="outline",
                orientation="horizontal",
                style={"height": "100%", "width": "100%"},
                value=tab,
                id="tabs-settings",
            ),
            html.Div(id="tabs-content", style={"paddingTop": 10}),
        ],
        pt=10,
        mt=20,
        # style={"paddingTop": 20, 'width': '100%'},
        className="dmc-container block-background",
        w="100%",
    )


@callback(Output("tabs-content", "children"), Input("tabs-settings", "value"))
def renderContent(active, test=True):
    if active == "files":
        conn = db_connection.getConn()
        categories = file_manager.getCategories(conn)
        settings = file_manager.getSettings(conn)
        return dmc.Stack(
            [
                html.H5("Каталоги"),
                dmc.TextInput(
                    label="Родительский каталог с папками",
                    style={"width": 250},
                    id="settings-catalog-main_folder",
                    value=(
                        settings["filemanager.baseway.test"]
                        if test
                        else settings["filemanager.baseway"]
                    ),
                    disabled=True,
                ),
                dbc.Button("Сохранить", style={"width": "min-content"}, disabled=True),
                dmc.Divider(variant="solid"),
                html.H5("Обновление библиотеки"),
                dmc.NumberInput(
                    label="Интервал обновления базы",
                    description="Указана периодичность в днях",
                    value=int(settings["filemanager.update_interval"]),
                    min=1,
                    style={"width": 250},
                    id="settings-catalog-update_interval",
                    disabled=True,
                ),
                dbc.Button("Сохранить", style={"width": "min-content"}, disabled=True),
                dmc.Divider(variant="solid"),
                html.H5("Категории"),
                dmc.MultiSelect(
                    label="Используемые категории файлов",
                    description="Категорией служит название подпапки в родительской папке с файлами. Обратите внимание, папки, у которых в начале стоит нижнее подчеркивание, не будут проанализированы.",
                    value=[i["category_name"] for i in categories],
                    data=[i["category_name"] for i in categories],
                    style={"width": 400, "marginBottom": 10},
                    id="settings-catalog-all_categories",
                    disabled=True,
                ),
                dmc.MultiSelect(
                    label="Категории с видеоконтентом",
                    description="Для выбранных категорий будет доступен просмотр видео в браузере",
                    value=[
                        i["category_name"]
                        for i in categories
                        if i["main_mime_type_id"] == 9
                    ],
                    data=[i["category_name"] for i in categories],
                    style={"width": 400, "marginBottom": 10},
                    id="settings-catalog-video_categories",
                    disabled=True,
                ),
                dmc.Group(
                    [
                        dbc.Button(
                            "Сохранить изменения",
                            id="settings-catalog-update_by_categories",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                    ],
                    style={"width": "max-content"},
                ),
                dmc.Divider(variant="solid"),
                html.H5("Кнопки управления"),
                dmc.Group(
                    [
                        dbc.Button(
                            "Пересканировать библиотеку файлов",
                            id="settings-catalog-manual_update",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dbc.Button(
                            "Пересканировать типы категорий",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dbc.Button(
                            "Пересканировать категории",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dbc.Button(
                            "Сброс базы файлового менеджера",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                        dbc.Button(
                            "Отключить файловый менеджер",
                            id="settings-catalog-disable_update",
                            style={"width": "max-content"},
                            disabled=True,
                        ),
                    ]
                ),
                dmc.Divider(variant="solid"),
                # html.H5("Лог обновления базы"),
                # dbc.Button(
                #     "Получить лог",
                #     id="settings-catalog-get_log",
                #     style={"width": "max-content"},
                # ),
            ]
        )
    elif active == "server_info":
        return [
            dmc.Space(h=5),
            dbc.Table(
                [
                    html.Tbody(
                        getSystemInfoRows()
                        + getCPUInfoRows()
                        + getRAMSWARInfoRows()
                        + getPartitionsInfoRows()
                    ),
                ],
                style={"table-layout": "auto", "width": "100%"},
            ),
        ]
    elif active == "widgets":
        return dmc.Stack(
            [
                html.H5("Погода"),
                dmc.TextInput(
                    label="Город, для которого нужно отображать погоду",
                    style={"width": 250},
                    id="widgets-weather-city",
                    value="Среднеуральск",
                    disabled=True,
                ),
                dbc.Button("Сохранить", style={"width": "min-content"}),
                dmc.Divider(variant="solid"),
                html.H5("Размеры разделов"),
                dmc.MultiSelect(
                    label="Выберите разделы, для которых будут отображаться их размеры на главном экране",
                    value=[
                        "/mnt/sdb1/",
                        "/mnt/sdc1/",
                        "/mnt/sdd1/",
                    ],
                    data=[
                        "/mnt/sdb1/",
                        "/mnt/sdc1/",
                        "/mnt/sdd1/",
                    ],
                    style={"width": 400},
                    id="widgets-partitions-selected",
                    disabled=True,
                ),
                dbc.Button("Сохранить", style={"width": "min-content"}),
                dmc.Divider(variant="solid"),
                html.H5("Системный монитор"),
                dmc.Text(
                    "Выберите те параметры, которые будут отображаться на главном экране"
                ),
                dmc.Stack(
                    children=[
                        dmc.Checkbox(
                            label="Загрузка CPU", checked=True, disabled=True, m=0
                        ),
                        dmc.Checkbox(
                            label="Загрузка RAM", checked=True, disabled=True, m=0
                        ),
                        dmc.Checkbox(
                            label="Загрузка SWAP", checked=True, disabled=True, m=0
                        ),
                        dmc.Checkbox(
                            label="Текущая скорость подключения",
                            checked=True,
                            disabled=True,
                            m=0,
                        ),
                        dbc.Button("Сохранить", style={"width": "min-content"}),
                    ],
                    mr="auto",
                    align="flex-start",
                ),
                dmc.Divider(variant="solid"),
                html.H5("Мониторинг торрентов"),
                dmc.Switch(
                    # size="lg",
                    # radius="sm",
                    label="Включить",
                    checked=True,
                    disabled=True,
                ),
                dmc.TextInput(
                    label="IP адрес сервера qBittorrent",
                    style={"width": 250},
                    value="192.168.3.33",
                    disabled=True,
                ),
                dmc.TextInput(
                    label="Порт сервера qBittorrent",
                    style={"width": 250},
                    value="8124",
                    disabled=True,
                ),
                dmc.TextInput(
                    label="Логин сервера qBittorrent",
                    style={"width": 250},
                    disabled=True,
                ),
                dmc.PasswordInput(
                    label="Пароль сервера qBittorrent",
                    style={"width": 250},
                    disabled=True,
                ),
                dbc.Button("Сохранить", style={"width": "min-content"}),
                dmc.Divider(variant="solid"),
            ],
            # w='100%'
        )
    else:
        # main
        return [
            dmc.Space(h=5),
            dmc.Stack(
                children=[
                    # dmc.TextInput(label="Какое-то поле ввода"),
                ],
            ),
        ]


@callback(
    [
        Output("cpu-ring-usage", "children"),
    ],
    [Input("show-cpu-load", "n_clicks")],
    prevent_initial_call=True,
)
def getCpuLoadRings(_):
    return [
        dmc.Group(
            [
                dmc.RingProgress(
                    sections=[
                        {
                            "value": percentage,
                            "color": "var(--bs-blue)",
                            "tooltip": f"{percentage}%",
                        },
                    ],
                    label=dmc.Text(
                        f"CPU{i}",
                        c="black",
                        ta="center",
                    ),
                    size=100,
                    roundCaps=True,
                )
                for i, percentage in enumerate(
                    psutil.cpu_percent(percpu=True, interval=0.1)
                )
            ]
        )
    ]
