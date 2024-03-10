# type - youtube/films/serials/apps
# category - название канала/жанра фильмов/общей категории приложений
# filename - название файла

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
import sqlite3
from dash_iconify import DashIconify
import time
import dash_bootstrap_components as dbc
from flask import request
from datetime import datetime
from utils import sql_traceback_generator

register_page(__name__, path="/search", icon="fa-solid:home")
videos_categories = [
    "cartoon_serials",
    "en_serials",
    "tv_shows",
    "youtube",
    "films",
    "ru_serials",
]


def get_icon(icon, size=18, background=True, icon_color="white"):
    """
    param:  \n
    `icon`: icon name
    """
    return (
        dmc.ThemeIcon(
            DashIconify(icon=icon, width=size, color=icon_color),
            size=size,
            radius=size + 7,
            # variant="subtle",
            color="#000000",
            m="5px",
        )
        if background == True
        else DashIconify(icon=icon, width=size, color=icon_color)
    )


def str_hider(name, limiter=25):
    """
    Сокращение строки до 30 символов, если не задано иное

    Параметры:
    ----------
    - name (str): сокращаемый текст
    - limiter (int): кол-во оставляемых символов (по умолчанию 30)
    """
    if len(name) <= limiter:
        return name
    else:
        return name[0:limiter] + "..."


def link_builder(server_link, name, hash, filetype, category, filename):
    """
    Генерация ссылок в файловом хранилище сервера

    Параметры:
    ----------
    - server_link - текущий адрес сервера
    - name - текст ссылки
    - hash - хэш файла на сервере
    - filetype - тип контента
    - category - категория контента
    - filename - название файла
    """
    return (
        dbc.Button(
            children=[
                (
                    get_icon("mdi:youtube")
                    if filetype == "youtube"
                    else get_icon("ic:movie")
                ),
                str_hider(name),
            ],
            style={"text-align": "center", "display": "flex", "align-items": "center"},
            outline=True,
            size="sm",
            href=f"/players/videoplayer?v={hash}&v_type={filetype}&l=y",
            className="link-primary",
        )
        if filetype in videos_categories and ".mp4" in filename
        else dbc.Button(
            children=[get_icon("ic:baseline-download"), str_hider(name)],
            style={"text-align": "center", "display": "flex", "align-items": "center"},
            outline=True,
            size="sm",
            href=f"http://{server_link}/storage/{filetype}/{category}/{filename}",
            download=filename,
            className="link-primary",
        )
    )


def search_link(filetype, category):
    """
    Получение ссылки на формирование поискового запроса

    Параметры:
    - filetype - тип файла
    - category - категория
    """
    return dbc.Button(
        children=[
            get_icon("mdi:youtube") if filetype == "youtube" else None,
            str_hider(category),
        ],
        style={"text-align": "center", "display": "flex", "align-items": "center"},
        outline=True,
        size="sm",
        href=f"/search?query={category}&from_video_view=True&l=y&search_category={filetype}",
        className="link-primary",
    )


def get_duration(seconds_data):
    return time.strftime("%H:%M:%S", time.gmtime(float(seconds_data)))


def get_size_str(size):
    size = float(size)
    if size <= 512:
        return str(size) + " MB"
    else:
        return str(round(size / 1024, 2)) + " GB"


def layout(
    l="n",
    query="",
    from_video_view="False",
    search_category="youtube",
    **other_unknown_query_strings,
):
    if l == "n":
        return dmc.Container()
    if from_video_view == "False":
        value_for_radio = "search_by_name"
    else:
        value_for_radio = "search_by_category"

    # print(query)
    if other_unknown_query_strings != {}:
        print(other_unknown_query_strings)

    return dmc.Container(
        children=[
            html.Div(id="notifications-container"),
            dmc.Space(h=10),
            dmc.Grid(
                children=[
                    # dmc.Col(span="auto"),
                    dmc.Col(
                        children=[
                            html.Div(
                                children=[
                                    html.H3("Поиск"),
                                    dmc.Space(h=10),
                                    dmc.Stack(
                                        children=[
                                            html.Div(
                                                [
                                                    dbc.Label("Поисковый запрос"),
                                                    dbc.Input(
                                                        id="search_query",
                                                        type="text",
                                                        value=str(query),
                                                        style={"width": "100%"},
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Категории для поиска"),
                                                    dbc.RadioItems(
                                                        options=[
                                                            {
                                                                "label": "YouTube",
                                                                "value": "youtube",
                                                            },
                                                            {
                                                                "label": "Фильмы",
                                                                "value": "films",
                                                            },
                                                            {
                                                                "label": "Мультсериалы",
                                                                "value": "cartoon_serials",
                                                            },
                                                            {
                                                                "label": "ТВ Шоу",
                                                                "value": "tv_shows",
                                                            },
                                                            {
                                                                "label": "Русские сериалы",
                                                                "value": "ru_serials",
                                                            },
                                                            {
                                                                "label": "Программы",
                                                                "value": "apps",
                                                            },
                                                        ],
                                                        value=search_category,
                                                        id="search_in_type",
                                                        inline=True,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Поиск по..."),
                                                    dbc.RadioItems(
                                                        options=[
                                                            {
                                                                "label": "Названию",
                                                                "value": "search_by_name",
                                                            },
                                                            {
                                                                "label": "Каналу / Категории",
                                                                "value": "search_by_category",
                                                            },
                                                        ],
                                                        value=value_for_radio,
                                                        id="search_by",
                                                        inline=True,
                                                    ),
                                                ]
                                            ),
                                            dmc.Space(h=3),
                                            dbc.Button("Поиск", id="search_button"),
                                        ]
                                    ),
                                ],
                                className="block-background",
                                style={"width": "100%"},
                            ),
                            dmc.Space(h=15),
                            dmc.LoadingOverlay(
                                html.Div(
                                    children=[
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        html.H3(
                                                            "Результаты поиска",
                                                            style={
                                                                "margin-bottom": "0"
                                                            },
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(span="auto"),
                                                dmc.Col(
                                                    dmc.Tooltip(
                                                        label="Количество результатов поиска ограничено - 500.",
                                                        position="bottom",
                                                        offset=3,
                                                        withArrow=True,
                                                        children=[
                                                            get_icon(
                                                                "material-symbols:info",
                                                                size=25,
                                                                icon_color="black",
                                                                background=False,
                                                            )
                                                        ],
                                                    ),
                                                    span="content",
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        dmc.Space(h=10),
                                        html.Div(id="table_search", style={'overflow-x': 'auto'}),
                                    ],
                                    id="results_loader",
                                    className="block-background",
                                    style={"width": "100%", "min-height": "100px"},
                                ),
                                loaderProps={
                                    "variant": "bars",
                                    "color": "--bs-primary",
                                    "size": "xl",
                                },
                            ),
                        ],
                    ),
                ]
            ),
        ],
        pt=20,
        style={"paddingTop": 20},
    )


@callback(
    [
        Output("table_search", "children"),
        Output("notifications-container", "children"),
        Output("results_loader", "children"),
    ],
    [
        State("search_by", "value"),
        State("search_query", "value"),
        State("search_in_type", "value"),
    ],
    [Input("search_button", "n_clicks")],
    prevent_initial_call=False,
)
def table_results(search_by, search_query, search_in_filetype, n_clicks):
    server_link = request.base_url.replace(":81", "").split("/")[2]
    if search_query == "":
        return "Введен пустой поисковый запрос", None
    else:
        if search_by == "search_by_category":
            column = "type"
        else:
            column = "filename"

        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S")

        start_time = time.time()
        try:
            conn = sqlite3.connect("bases/nstorage.sqlite3")
            c = conn.cursor()
            # c.execute(f"SELECT * FROM {search_in_filetype} WHERE {column} LIKE '%{search_query}%'")
            c.execute(
                f"SELECT * FROM {search_in_filetype} WHERE {column} LIKE '%{search_query}%' LIMIT 500"
            )
            results = c.fetchall()
            c.close()
            conn.close()
        except sqlite3.Error as er:
            err_cont = sql_traceback_generator.gen(er, from_search=True)
            notif = dmc.Notification(
                title="Ошибка выполнения запроса",
                id="my-notif",
                action="show",
                message="Подробности на экране",
                icon=DashIconify(icon="ep:warning-filled"),
                color="red",
            )
            return err_cont, notif

        table_header = [
            html.Thead(
                html.Tr(
                    [
                        # html.Th("Источник"),
                        html.Th("Канал / Категория"),
                        html.Th("Название"),
                        html.Th("Размер"),
                        (
                            html.Th("Длительность")
                            if search_in_filetype in videos_categories
                            else None
                        ),
                    ]
                )
            )
        ]

        table_content = []
        for result_line in results:
            category = result_line[2]
            filename = result_line[3]
            name = ".".join(filename.split(".")[:-1])
            table_content += [
                html.Tr(
                    [
                        # html.Td(search_in_filetype),
                        html.Td(search_link(search_in_filetype, category)),
                        html.Td(
                            link_builder(
                                server_link,
                                name,
                                result_line[1],
                                search_in_filetype,
                                category,
                                filename,
                            )
                        ),
                        html.Td(get_size_str(result_line[5])),
                        (
                            html.Td(get_duration(result_line[6]))
                            if search_in_filetype in videos_categories
                            else None
                        ),
                    ]
                )
            ]

        table_content = [html.Tbody(table_content)]

        print(
            f'{request.remote_addr} - - [{now}] | search | {search_by} | category "{search_in_filetype}" | query "{search_query}" | results {len(results)} | time {round(time.time() - start_time, 3)}'
        )

        return (
            (
                [dmc.Table(table_header + table_content)]
                if len(results) > 0
                else [dmc.Center([html.H5("По Вашему запросу нет результатов.")])]
            ),
            dmc.Notification(
                title="Запрос выполнен",
                id="my-notif",
                action="show",
                message=f"Результаты получены за {round(time.time() - start_time, 3)} секунд. Результатов {len(results)}",
                icon=DashIconify(icon="ep:success-filled"),
            ),
            no_update,
        )
