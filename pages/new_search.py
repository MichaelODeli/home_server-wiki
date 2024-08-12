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
                        dmc.GridCol(span="auto", className="hided_element"),
                        dmc.GridCol(
                            [
                                html.Div(
                                    children=[
                                        dmc.TextInput(
                                            label="Поисковый запрос",
                                            id="n_search_query",
                                            value=str(query),
                                            style={"width": "100%"},
                                            pe="md",
                                        ),
                                        dmc.Space(h=10),
                                        dmc.Accordion(
                                            variant="filled",
                                            chevronPosition="left",
                                            children=[
                                                dmc.AccordionItem(
                                                    [
                                                        dmc.AccordionControl(
                                                            dmc.Text(
                                                                "Дополнительные параметры",
                                                                c="var(--bs-body-color)",
                                                            )
                                                        ),
                                                        dmc.AccordionPanel(
                                                            [
                                                                dmc.Divider(
                                                                    label="Фильтры для поиска",
                                                                    labelPosition="left",
                                                                    h="lg",
                                                                ),
                                                                dmc.Grid(
                                                                    [
                                                                        dmc.GridCol(
                                                                            [
                                                                                dmc.MultiSelect(
                                                                                    w="100%",
                                                                                    searchable=True,
                                                                                    hidePickedOptions=True,
                                                                                    clearable=True,
                                                                                    label="Категория для поиска",
                                                                                    id="n_search_in_category",
                                                                                    placeholder="Поиск по всем категориям",
                                                                                    data=category_select_data,
                                                                                    value=[],
                                                                                )
                                                                            ],
                                                                            span=6,
                                                                            className="adaptive-container",
                                                                        ),
                                                                        dmc.GridCol(
                                                                            [
                                                                                dmc.MultiSelect(
                                                                                    w="100%",
                                                                                    searchable=True,
                                                                                    hidePickedOptions=True,
                                                                                    clearable=True,
                                                                                    label="Типы для поиска",
                                                                                    id="n_search_in_types",
                                                                                    placeholder="Поиск по всем типам",
                                                                                    disabled=True,
                                                                                    value=[],
                                                                                )
                                                                            ],
                                                                            span=6,
                                                                            className="adaptive-container",
                                                                        ),
                                                                    ],
                                                                    w="100%",
                                                                    justify="center",
                                                                    className="adaptive-grid",
                                                                ),
                                                                dmc.Space(h="md"),
                                                                dmc.Divider(
                                                                    label="Опции для отображения результатов",
                                                                    labelPosition="left",
                                                                    h="md",
                                                                ),
                                                                dmc.Space(h="md"),
                                                                dmc.Group(
                                                                    [
                                                                        dmc.Chip(
                                                                            "Открывать поддерживаемые "
                                                                            "медиафайлы во встроенном плеере",
                                                                            checked=False,
                                                                            disabled=True,
                                                                        ),
                                                                        dmc.Chip(
                                                                            "Открывать медиафайлы в VLC "
                                                                            "(mobile)",
                                                                            checked=False,
                                                                            disabled=True,
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                    value="info",
                                                ),
                                            ],
                                        ),
                                        dmc.Button(
                                            "Поиск",
                                            id="n_search_button",
                                            n_clicks=0,
                                            fullWidth=True,
                                        ),
                                    ],
                                    className="block-background",
                                    style={"width": "100%"},
                                ),
                                dmc.Space(h=15),
                                html.Div(
                                    dmc.Stack(
                                        children=[
                                            html.H3(
                                                "Результаты поиска",
                                                style={"margin-bottom": "0"},
                                            ),
                                            dmc.Space(h=10),
                                            html.Div(
                                                id="n_search_results",
                                                style={"overflow-x": "auto"},
                                            ),
                                            dmc.Space(h=10),
                                            dmc.Pagination(
                                                total=1,
                                                value=1,
                                                siblings=1,
                                                withControls=True,
                                                withEdges=True,
                                                id="search_pagination",
                                            ),
                                        ],
                                        id="results_loader",
                                        className="block-background",
                                        style={"width": "100%", "min-height": "100px"},
                                        gap="xs",
                                    ),
                                ),
                            ],
                            span=10,
                            className="adaptive-container",
                        ),
                        dmc.GridCol(span="auto", className="hided_element"),
                    ],
                    className="adaptive-grid",
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
    Output("search_pagination", "total"),
    Input("search_pagination", "value"),
    Input("n_search_button", "n_clicks"),
    State("n_search_in_category", "value"),
    State("n_search_in_types", "value"),
    State("n_search_query", "value"),
    prevent_initial_call=True,
)
def search(current_page, n_clicks, categories, types, query, test=True):

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

    conn = db_connection.get_conn()

    current_page -= 1

    PAGE_LIMIT = 20
    OFFSET = current_page * PAGE_LIMIT

    # check inputs and get results
    if (query == None or query == "") and (
        categories == [] or (categories == [] and types == [])
    ):
        return no_update, notif_empty_input, 1
    elif (query != None and query != "") and (categories == [] and types == []):
        counter, query_results = file_manager.get_filesearch_result(
            conn,
            mode="all",
            query=query,
            limit=PAGE_LIMIT,
            offset=OFFSET,
        )

        returner = ["Поиск по всей библиотеке файлов", no_update]
    elif (query != None and query != "") and (categories != [] and types == []):
        counter, query_results = file_manager.get_filesearch_result(
            conn,
            mode="by_category",
            query=query,
            categories=categories,
            limit=PAGE_LIMIT,
            offset=OFFSET,
        )

        returner = ["Поиск по определенной категории", no_update]
    elif (query == None or query == "") and (categories != [] and types == []):
        counter, query_results = file_manager.get_filesearch_result(
            conn,
            mode="all_from_category",
            categories=categories,
            limit=PAGE_LIMIT,
            offset=OFFSET,
        )

        returner = ["Отображаем все файлы категории", no_update]
    elif (query == None or query == "") and (categories != [] and types != []):
        counter, query_results = file_manager.get_filesearch_result(
            conn,
            mode="all_from_category_type",
            categories=categories,
            types=types,
            limit=PAGE_LIMIT,
            offset=OFFSET,
        )

        returner = ["Отображаем все файлы из категории и типа", no_update]
    elif (query != None and query != "") and (categories != [] and types != []):
        counter, query_results = file_manager.get_filesearch_result(
            conn,
            mode="by_category_type_query",
            query=query,
            categories=categories,
            types=types,
            limit=PAGE_LIMIT,
            offset=OFFSET,
        )

        returner = ["Отображаем файлы из категории и типа по запросу", no_update]
    else:
        return "Ошибочка", no_update

    if counter == 0:
        return html.H6("По Вашему запросу результатов нет"), no_update, 1
    else:
        pages = (
            int(counter / PAGE_LIMIT) + 1
            if counter % PAGE_LIMIT != 0
            else counter / PAGE_LIMIT
        )

        rows = [
            dmc.TableTr(
                [
                    dmc.TableTd(element["category_name"]),
                    dmc.TableTd(element["type_name"]),
                    dmc.TableTd(
                        html.A(
                            element["file_name"],
                            href="http://" + element["file_fullway_forweb"],
                        )
                    ),
                ]
            )
            for element in query_results
        ]

        head = dmc.TableThead(
            dmc.TableTr(
                [
                    dmc.TableTh("Категория", className="sticky-th"),
                    dmc.TableTh("Тип", className="sticky-th"),
                    dmc.TableTh("Файл", className="sticky-th"),
                ]
            )
        )
        body = dmc.TableTbody(rows)

        return dmc.Table([head, body]), no_update, pages

    # print(
    #     "found",
    #     counter,
    #     "results /",
    #     returner[0],
    #     "/ offset",
    #     OFFSET,
    #     "/ data len",
    #     len(query_results),
    # )

    # return returner + [pages]
