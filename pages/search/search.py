# type - youtube/films/serials/apps
# category - название канала/жанра фильмов/общей категории приложений
# filename - название файла

# params
setting_min_search_len = 3
setting_search_output_limit = 500
videos_categories = [
    "cartoon_serials",
    "en_serials",
    "tv_shows",
    "youtube",
    "films",
    "ru_serials",
]


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
from controllers import cont_search as cont_s
from controllers import service_controller as service

register_page(__name__, path="/search", icon="fa-solid:home")


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

    service.log_printer(request.remote_addr, 'search', 'page opened')

    return dmc.Container(
        children=[
            html.Div(id="notifications-container"),
            dmc.Space(h=10),
            dmc.Grid(
                children=[
                    dmc.GridCol(span="auto"),
                    dmc.GridCol(
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
                            html.Div(
                            # dmc.LoadingOverlay(
                                html.Div(
                                    children=[
                                        dmc.Grid(
                                            [
                                                dmc.GridCol(
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
                                                dmc.GridCol(span="auto"),
                                                dmc.GridCol(
                                                    dmc.Tooltip(
                                                        label="Количество результатов поиска ограничено - 500.",
                                                        position="bottom",
                                                        offset=3,
                                                        withArrow=True,
                                                        children=[
                                                            cont_s.get_icon(
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
                                # loaderProps={
                                #     "variant": "bars",
                                #     "color": "--bs-primary",
                                #     "size": "xl",
                                # },
                            ),
                        ],
                        span=10
                    ),
                    dmc.GridCol(span="auto"),
                ]
            ),
        ],
        pt=20,
        # style={"paddingTop": 20},
        className='dmc-container',
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
)
def table_results(search_by, search_query, search_in_filetype, n_clicks):
    global setting_min_search_len
    global setting_search_output_limit

    server_link = request.base_url.replace(":81", "").split("/")[2]
    if search_query == "":
        return "Введен пустой поисковый запрос", None
    elif len(search_query) <= setting_min_search_len: 
        return f"Минимальное количество символов для поиска - {str(setting_min_search_len)}", no_update, no_update
    else:
        if search_by == "search_by_category":
            column = "type"
        else:
            column = "filename"

        start_time = time.time()
        try:
            conn = sqlite3.connect("bases/nstorage.sqlite3")
            c = conn.cursor()
            # c.execute(f"SELECT * FROM {search_in_filetype} WHERE {column} LIKE '%{search_query}%'")
            c.execute(
                f"SELECT * FROM {search_in_filetype} WHERE {column} LIKE '%{search_query}%' LIMIT {str(setting_search_output_limit)}"
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
                        html.Td(cont_s.search_link(search_in_filetype, category)),
                        html.Td(
                            cont_s.link_builder(
                                server_link,
                                name,
                                result_line[1],
                                search_in_filetype,
                                category,
                                filename,
                            )
                        ),
                        html.Td(cont_s.get_size_str(result_line[5])),
                        (
                            html.Td(cont_s.get_duration(result_line[6]))
                            if search_in_filetype in videos_categories
                            else None
                        ),
                    ]
                )
            ]

        table_content = [html.Tbody(table_content)]


        service.log_printer(request.remote_addr, 'search', f'{search_by} | category "{search_in_filetype}" | query "{search_query}" | results {len(results)} | time {round(time.time() - start_time, 3)}')
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
                icon=DashIconify(icon="ep:success-filled")
            ),
            no_update,
        )
