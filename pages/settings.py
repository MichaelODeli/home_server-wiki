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
import psutil
import platform

register_page(__name__, path="/settings", icon="fa-solid:home")


def generate_tablerow(param_name, param_value="", head=False):
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


def get_size(bytes, suffix="B"):
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


def get_system_info_rows():
    uname = platform.uname()
    return [
        generate_tablerow(html.H6("Информация о системе")),
        generate_tablerow("Операционная система", f"{uname.system}"),
        generate_tablerow("Идентификатор устройства", f"{uname.node}"),
        generate_tablerow("Релиз", f"{uname.release}"),
        generate_tablerow("Версия ОС", f"{uname.version}"),
        generate_tablerow("Архитектура", f"{uname.machine}"),
        generate_tablerow("Процессор", f"{uname.processor}"),
    ]


def get_cpu_info_rows():
    cpufreq = psutil.cpu_freq()
    return [
        generate_tablerow(html.H6("Информация о процессоре")),
        generate_tablerow(
            "Физических/логических ядер",
            f"{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}",
        ),
        generate_tablerow(
            "Базовая частота",
            f"{cpufreq.current:.2f}Mhz",
        ),
        generate_tablerow(
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
        generate_tablerow(
            "Использование процессора",
            f"{psutil.cpu_percent()}%",
        ),
    ]


def get_ram_swap_info_rows():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return [
        generate_tablerow(html.H6("ОЗУ")),
        generate_tablerow("Всего", f"{get_size(svmem.total)}"),
        generate_tablerow(
            "Доступно",
            f"{get_size(svmem.available)}",
        ),
        generate_tablerow("Использовано", f"{get_size(svmem.used)}"),
        generate_tablerow("Процент использования", f"{svmem.percent}%"),
        generate_tablerow(html.H6("SWAP")),
        generate_tablerow("Всего", f"{get_size(swap.total)}"),
        generate_tablerow("Свободно", f"{get_size(swap.free)}"),
        generate_tablerow("Использовано", f"{get_size(swap.used)}"),
        generate_tablerow("Процент использования", f"{swap.percent}%"),
    ]


def get_partitions_info_rows():
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
                dcc.Markdown(f"**Всего доступно**: {get_size(partition_usage.total)}")
            )
            partition_data.append(
                dcc.Markdown(f"**Использовано**: {get_size(partition_usage.used)}")
            )
            partition_data.append(
                dcc.Markdown(f"**Свободно**: {get_size(partition_usage.free)}")
            )
            partition_data.append(
                dcc.Markdown(f"**Процент использования**: {partition_usage.percent}%")
            )
        except PermissionError:
            continue
        parts_data.append(
            generate_tablerow(partition.device, dmc.Stack(partition_data, gap="xs"))
        )

    return [generate_tablerow(html.H6("Накопители и разделы"))] + parts_data


def layout(l="n", tab="server_info", **kwargs):
    if l == "n":
        return dmc.Container()
    service.log_printer(request.remote_addr, "settings", "page opened")

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
def render_content(active):
    if active == "files":
        return dmc.Stack(
            [
                html.H5("Каталоги"),
                dmc.TextInput(
                    label="Родительский каталог с папками",
                    style={"width": 250},
                    id="settings-catalog-main_folder",
                ),
                dbc.Button("Сохранить", style={"width": "min-content"}),
                dmc.Divider(variant="solid"),
                html.H5("Обновление библиотеки"),
                dmc.NumberInput(
                    label="Интервал обновления базы",
                    description="Указана периодичность в днях",
                    value=1,
                    min=1,
                    style={"width": 250},
                    id="settings-catalog-update_interval",
                ),
                dbc.Button("Сохранить", style={"width": "min-content"}),
                dmc.Divider(variant="solid"),
                html.H5("Категории"),
                dmc.MultiSelect(
                    label="Используемые категории файлов",
                    description="Категорией служит название подпапки в родительской папке с файлами. Обратите внимание, папки, у которых в начале стоит нижнее подчеркивание, не будут проанализированы.",
                    value=[
                        "cartoon_serials",
                        "en_serials",
                        "apps",
                        "books",
                        "tv_shows",
                        "youtube",
                        "films",
                    ],
                    data=[
                        "history",
                        "cartoon_serials",
                        "en_serials",
                        "data_science",
                        "apps",
                        "books",
                        "tv_shows",
                        "youtube",
                        "films",
                        "wiki",
                    ],
                    style={"width": 400, "marginBottom": 10},
                    id="settings-catalog-all_categories",
                ),
                dmc.MultiSelect(
                    label="Категории с видеоконтентом",
                    description="Для выбранных категорий будет доступен просмотр видео через отдельную страницу /videoview",
                    value=[
                        "cartoon_serials",
                        "en_serials",
                        "tv_shows",
                        "youtube",
                        "films",
                        "ru_serials",
                    ],
                    data=[
                        "history",
                        "cartoon_serials",
                        "en_serials",
                        "data_science",
                        "apps",
                        "books",
                        "tv_shows",
                        "youtube",
                        "films",
                        "wiki",
                    ],
                    style={"width": 400, "marginBottom": 10},
                    id="settings-catalog-video_categories",
                ),
                dmc.Group(
                    [
                        dbc.Button(
                            "Обновить библиотеку по выбранным категориям",
                            id="settings-catalog-update_by_categories",
                            style={"width": "max-content"},
                        ),
                        dbc.Button(
                            "Повторное сканирование категорий",
                            id="settings-catalog-scan_categories",
                            style={"width": "max-content"},
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
                        ),
                        dbc.Button(
                            "Отключить файловый менеджер",
                            id="settings-catalog-disable_update",
                            style={"width": "max-content"},
                        ),
                    ]
                ),
                dmc.Divider(variant="solid"),
                html.H5("Лог обновления базы"),
                dbc.Button(
                    "Получить лог",
                    id="settings-catalog-get_log",
                    style={"width": "max-content"},
                ),
            ]
        )
    elif active == "server_info":
        return [
            dmc.Space(h=5),
            dbc.Table(
                [
                    html.Tbody(
                        get_system_info_rows()
                        + get_cpu_info_rows()
                        + get_ram_swap_info_rows()
                        + get_partitions_info_rows()
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
def get_cpu_load_rings(_):
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
