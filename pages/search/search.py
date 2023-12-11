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

register_page(__name__, path="/search", icon="fa-solid:home")

def str_hider(name, limiter=30):
    """
    Сокращение имени файла до 30 символов, если не задано иное

    Параметры:
    ----------
    - name (str): сокращаемый текст
    - limiter (int): кол-во оставляемых символов (по умолчанию 30)
    """
    if len(name) <= limiter:
        return name
    else:
        return name[0:limiter] + "..."

def link_builder(name, hash, filetype, category, filename):
    return (
        html.A(
            str_hider(name),
            href=f"/players/videoplayer?v={hash}&v_type={filetype}",
        )
        if filetype in ["films", "youtube"]
        else html.A(
            str_hider(name),
            href=f"http://192.168.3.33/storage/{filetype}/{category}/{filename}",
        )
    )

def layout(query="", from_video_view="False", **other_unknown_query_strings):
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
                                            dmc.TextInput(
                                                label="Поисковый запрос",
                                                style={"width": "100%"},
                                                value=str(query),
                                                id="search_query",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Категории для поиска"),
                                                    dbc.RadioItems(
                                                        options=[
                                                            {"label": "YouTube", "value": 'youtube'},
                                                            {"label": "Фильмы", "value": 'films'},
                                                            {"label": "Программы", "value": 'apps'},
                                                        ],
                                                        value='youtube',
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
                                                            {"label": "Названию", "value": 'search_by_name'},
                                                            {"label": "Каналу / Категории", "value": 'search_by_category'},
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
                                children=[
                                    html.H3("Результаты поиска"),
                                    dmc.Space(h=10),
                                    html.Div(id="table_search"),
                                ],
                                className="block-background",
                                style={"width": "100%"},
                            ),
                            # dmc.Space(h=15),
                            # html.Div(
                            #     children=[],
                            #     className="block-background",
                            # ),
                        ],
                        # span=3,
                    ),
                    # dmc.Col(span="auto"),
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
    if search_query == "":
        return "Введен пустой поисковый запрос", None
    else:
        if search_by == "search_by_category":
            column = "type"
        else:
            column = "filename"

        start_time = time.time()
        conn = sqlite3.connect("bases/nstorage.sqlite3")
        c = conn.cursor()
        c.execute(f"SELECT * FROM {search_in_filetype} WHERE {column} LIKE '%{search_query}%'")
        results = c.fetchall()

        table_header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Источник"),
                        html.Th("Канал / Категория"),
                        html.Th("Название"),
                    ]
                )
            )
        ]

        table_content = []
        for result_line in results:
            category = result_line[1]
            filename = result_line[2]
            name = ".".join(filename.split(".")[:-1])
            table_content += [
                html.Tr(
                    [
                        html.Td(search_in_filetype),
                        html.Td(str_hider(category)),
                        html.Td(link_builder(name, result_line[0], search_in_filetype, category, filename)),
                    ]
                )
            ]

        table_content = [html.Tbody(table_content)]

        c.close()
        conn.close()

        return (
            [dmc.Table(table_header + table_content)]
            if len(results) > 0
            else [dmc.Center([html.H5("По Вашему запросу нет результатов.")])],
            dmc.Notification(
                title="Запрос выполнен",
                id="my-notif",
                action="show",
                message="Результаты получены за %s секунд" % round(time.time() - start_time, 3),
                icon=DashIconify(icon="ep:success-filled"),
            )
        )
