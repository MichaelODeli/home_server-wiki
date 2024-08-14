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
from controllers import db_connection
from controllers import file_manager
from controllers import service_controller as service
from controllers import cont_search as cont_s
from dash.exceptions import PreventUpdate
import time

register_page(__name__, path="/search", icon="fa-solid:home")


def layout(
    l="n",
    query="",
    category_id=[],
    type_id=[],
    auto_search="n",
    **other_unknown_query_strings,
):
    if l == "n":
        return dmc.Container()
    else:
        service.log_printer(request.remote_addr, "search", "page opened")

        category_id = [category_id] if category_id != [] else category_id
        type_id = [type_id] if type_id != [] else type_id

        if auto_search != "n" and (query != "" or category_id != []):
            search_clicks = 1
        else:
            search_clicks = 0

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
                                                                                    value=category_id,
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
                                                                                    value=type_id,
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
                                                                dmc.RadioGroup(
                                                                    dmc.Stack(
                                                                        [
                                                                            dmc.Radio(
                                                                                label="Открывать поддерживаемые "
                                                                                "медиафайлы во встроенном плеере",
                                                                                value="open_mediafiles_in_internal_player",
                                                                            ),
                                                                            dmc.Radio(
                                                                                label="Открывать медиафайлы в VLC "
                                                                                "(mobile)",
                                                                                value="open_mediafiles_in_vlc",
                                                                            ),
                                                                            dmc.Radio(
                                                                                label="Стандартные прямые ссылки",
                                                                                value="full_links",
                                                                            ),
                                                                        ],
                                                                        gap="xs",
                                                                    ),
                                                                    value="full_links",
                                                                    id="mediafiles_links_format",
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
                                            n_clicks=search_clicks,
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
                                                "Результаты поиска", className="p-0 m-0"
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
    State("mediafiles_links_format", "value"),
    prevent_initial_call=True,
)
def search(
    current_page, n_clicks, categories, types, query, mediafiles_links_format, test=True
):

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

    start_time = time.time()
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
    elif (query != None and query != "") and (categories != [] and types == []):
        counter, query_results = file_manager.get_filesearch_result(
            conn,
            mode="by_category",
            query=query,
            categories=categories,
            limit=PAGE_LIMIT,
            offset=OFFSET,
        )
    elif (query == None or query == "") and (categories != [] and types == []):
        counter, query_results = file_manager.get_filesearch_result(
            conn,
            mode="all_from_category",
            categories=categories,
            limit=PAGE_LIMIT,
            offset=OFFSET,
        )
    elif (query == None or query == "") and (categories != [] and types != []):
        counter, query_results = file_manager.get_filesearch_result(
            conn,
            mode="all_from_category_type",
            categories=categories,
            types=types,
            limit=PAGE_LIMIT,
            offset=OFFSET,
        )
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
    else:
        return "Ошибочка", no_update, 1

    if counter == 0:
        return html.H6("По Вашему запросу результатов нет"), no_update, 1
    else:
        pages = (
            int(counter / PAGE_LIMIT) + 1
            if counter % PAGE_LIMIT != 0
            else counter / PAGE_LIMIT
        )

        result_notif = dmc.Notification(
            title="Запрос выполнен",
            id="my-notif",
            action="show",
            message=f"Результаты получены за {round(time.time() - start_time, 3)} секунд. Результатов {counter}",
            icon=DashIconify(icon="ep:success-filled"),
        )
        service.log_printer(
            request.remote_addr,
            "search",
            f'category {str(categories)} | type {str(types)} | query "{query}" | results {counter} | page {current_page} | time {round(time.time() - start_time, 3)}',
        )

        return (
            cont_s.format_search_results(
                query_results=query_results,
                mediafiles_links_format=mediafiles_links_format,
            ),
            result_notif,
            pages,
        )
