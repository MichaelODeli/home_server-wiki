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
from dash_iconify import DashIconify
import time
import dash_bootstrap_components as dbc
from flask import request
from datetime import datetime
from utils import sql_traceback_generator
from controllers import db_connection
from controllers import file_manager
from controllers import service_controller as service
from controllers import cont_search as cont_s
from dash.exceptions import PreventUpdate
from psycopg2.extensions import AsIs

register_page(__name__, path="/new_search", icon="fa-solid:home")


def layout(
    l="n",
    query="",
    **other_unknown_query_strings,
):
    if l == "n":
        return dmc.Container()
    else:
        conn = db_connection.get_conn()

        category_select_data = [
            {
                "label": (
                    i["category_pseudonym"]
                    if i["category_pseudonym"] != None
                    else i["category_name"]
                ),
                "value": str(i["category_id"]),
            }
            for i in file_manager.getCategories(conn)
        ]

        return dmc.Container(
            children=[
                dmc.Space(h=10),
                dmc.Grid(
                    [
                        dmc.GridCol(span="auto"),
                        dmc.GridCol(
                            [
                                html.Div(
                                    children=[
                                        html.H3("Поиск"),
                                        dmc.Space(h=10),
                                        dmc.Stack(
                                            children=[
                                                dmc.TextInput(
                                                    label="Поисковый запрос",
                                                    id="n_search_query",
                                                    value=str(query),
                                                    style={"width": "100%"},
                                                    description="Если будет задан пустой поисковый запрос - "
                                                    "будет отображен весь список файлов из данной категории/типа.",
                                                ),
                                                dmc.Group(
                                                    [
                                                        dmc.MultiSelect(
                                                            w="47%",
                                                            searchable=True,
                                                            hidePickedOptions=True,
                                                            clearable=True,
                                                            label="Категория для поиска",
                                                            id="n_search_in_category",
                                                            placeholder="Поиск по всем категориям",
                                                            data=category_select_data,
                                                            value=[],
                                                        ),
                                                        dmc.MultiSelect(
                                                            w="47%",
                                                            searchable=True,
                                                            hidePickedOptions=True,
                                                            clearable=True,
                                                            label="Типы для поиска",
                                                            id="n_search_in_types",
                                                            placeholder="Поиск по всем типам",
                                                            disabled=True,
                                                            value=[],
                                                        ),
                                                    ],
                                                    w="100%",
                                                    grow=True,
                                                    gap="xs",
                                                    justify="center",
                                                ),
                                                dmc.Space(h=3),
                                                dbc.Button(
                                                    "Поиск",
                                                    id="n_search_button",
                                                    n_clicks=0,
                                                ),
                                            ]
                                        ),
                                    ],
                                    className="block-background",
                                    style={"width": "100%"},
                                ),
                                dmc.Space(h=15),
                                html.Div(
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
                                            html.Div(
                                                id="n_search_results",
                                                style={"overflow-x": "auto"},
                                            ),
                                        ],
                                        id="results_loader",
                                        className="block-background",
                                        style={"width": "100%", "min-height": "100px"},
                                    ),
                                ),
                            ],
                            span=10,
                        ),
                        dmc.GridCol(span="auto"),
                    ]
                ),
            ],
            pt=20,
            className="dmc-container",
        )


@callback(
    Output("n_search_in_types", "data"),
    Output("n_search_in_types", "disabled"),
    Output("n_search_in_category", "placeholder"),
    Output("n_search_in_types", "placeholder"),
    Input("n_search_in_category", "value"),
    State("n_search_in_types", "value"),
)
def add_types_in_search(category_id, selected_types):
    if category_id == None or category_id == []:
        return no_update, True, "Поиск по всем категориям", "Поиск по всем типам"
    else:
        conn = db_connection.get_conn()

        types_select_data = []

        for single_c_id in category_id:
            single_c_id = int(single_c_id)
            found_category = file_manager.getCategories(conn, category_id=single_c_id)

            c_data = []

            if len(found_category) > 0:
                found_types = len(file_manager.getTypes(conn, category_id=single_c_id))
                if found_types > 0:
                    c_data += [
                        {
                            "label": (
                                i["type_pseudonym"]
                                if i["type_pseudonym"] != None
                                else i["type_name"]
                            ),
                            "value": str(i["type_id"]),
                        }
                        for i in file_manager.getTypes(conn, category_id=single_c_id)
                    ]

                    types_select_data += [
                        {"group": found_category[0]["category_name"], "items": c_data}
                    ]

        return (
            types_select_data,
            False,
            "Поиск по выбранным категориям",
            (
                "Поиск по выбранным типам"
                if len(selected_types) > 0
                else "Поиск по всем типам"
            ),
        )


@callback(
    Output("n_search_results", "children"),
    Output("notifications-container-search", "children"),
    Input("n_search_button", "n_clicks"),
    State("n_search_in_category", "value"),
    State("n_search_in_types", "value"),
    State("n_search_query", "value"),
    prevent_initial_call=True,
)
def search(n_clicks, categories, types, query, test=True):

    if n_clicks == 0:
        raise PreventUpdate

    notif_empty_input = dmc.Notification(
        title="Ошибка поиска",
        id="simple-notify-2",
        action="show",
        message="Введен пустой поисковый запрос.",
        color="red",
        # icon=DashIconify(icon="ic:round-celebration"),
    )

    sql_limit = 500
    sql_source = """select file_id, category_name, type_name, file_fullway_forweb, 
    file_name, mime_type, mime_type_id, size_kb, 
    html_video_ready, html_audio_ready, type_id, category_id 
    from filestorage_files_summary"""

    with db_connection.get_conn().cursor() as cursor:
        # check inputs and get results
        if (query == None or query == "") and (
            categories == [] or (categories == [] and types == [])
        ):
            return no_update, notif_empty_input
        elif (query != None and query != "") and (categories == [] and types == []):
            cursor.execute(
                sql_source
                + " WHERE LOWER(file_name) LIKE LOWER(%(query)s) LIMIT %(limit)s;",
                {"query": "%%" + query + "%%", "limit": sql_limit},
            )

            returner = ["Поиск по всей библиотеке файлов", no_update]
        elif (query != None and query != "") and (categories != [] and types == []):
            cursor.execute(
                sql_source
                + " WHERE LOWER(file_name) LIKE LOWER(%(query)s) and category_id in (%(categories)s) LIMIT %(limit)s;",
                {
                    "query": "%%" + query + "%%",
                    "categories": AsIs(", ".join(categories)),
                    "limit": sql_limit,
                },
            )

            returner = ["Поиск по определенной категории", no_update]
        elif (query == None or query == "") and (categories != [] and types == []):
            cursor.execute(
                sql_source + " WHERE category_id in (%(categories)s) LIMIT %(limit)s;",
                {"categories": AsIs(", ".join(categories)), "limit": sql_limit},
            )

            returner = ["Отображаем все файлы категории", no_update]
        elif (query == None or query == "") and (categories != [] and types != []):
            cursor.execute(
                sql_source
                + " WHERE category_id in (%(categories)s) and type_id in (%(types)s) LIMIT %(limit)s;",
                {
                    "categories": AsIs(", ".join(categories)),
                    "types": AsIs(", ".join(types)),
                    "limit": sql_limit,
                },
            )

            returner = ["Отображаем все файлы из категории и типа", no_update]
        elif (query != None and query != "") and (categories != [] and types != []):
            cursor.execute(
                sql_source
                + " WHERE LOWER(file_name) LIKE LOWER(%(query)s) and category_id in (%(categories)s) and type_id in (%(types)s) LIMIT %(limit)s;",
                {
                    "query": "%%" + query + "%%",
                    "categories": AsIs(", ".join(categories)),
                    "types": AsIs(", ".join(types)),
                    "limit": sql_limit,
                },
            )

            returner = ["Отображаем файлы из категории и типа по запросу", no_update]
        else:
            return "Ошибочка", no_update

        # get query result as dict
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

        if len(data) > 0:
            print(f"found {len(data)} results")
            print(data[0])
        else:
            print("not found")

        return returner
