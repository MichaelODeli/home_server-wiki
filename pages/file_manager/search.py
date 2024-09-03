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
from controllers import cont_search
from dash.exceptions import PreventUpdate
import time

register_page(__name__, path="/search", icon="fa-solid:home")


def layout(
    l="n",
    query="",
    category_id=[],
    type_id=[],
    auto_search="n",
    from_video="n",
    **other_unknown_query_strings,
):
    if l == "n":
        return dmc.Container()
    else:
        service.logPrinter(request.remote_addr, "search", "page opened")

        category_id , type_id = cont_search.formatCategoryType(category_id, type_id)

        if auto_search != "n" and (query != "" or category_id != []):
            search_clicks = 1
        else:
            search_clicks = 0

        conn = db_connection.getConn()

        category_select_data = cont_search.getCategoriesForMultiSelect(conn)

        return dmc.Container(
            children=[
                dmc.Space(h=10),
                dmc.Grid(
                    [
                        dmc.GridCol(span="auto", className="hided_element"),
                        dmc.GridCol(
                            [
                                dmc.Card(
                                    children=[
                                        dmc.TextInput(
                                            label="Поисковый запрос",
                                            id="n_search_query",
                                            value=str(query),
                                            style={"width": "100%"},
                                            pe="md",
                                        ),
                                        dmc.Space(h=10),
                                        cont_search.getSearchAccordion(category_id, type_id, category_select_data, from_video=False),
                                        dmc.Button(
                                            "Поиск",
                                            id="n_search_button",
                                            n_clicks=search_clicks,
                                            fullWidth=True,
                                        ),
                                    ],
                                    shadow="sm",
                                    w='100%'
                                ),
                                dmc.Space(h=15),
                                dmc.Card(
                                    dmc.Stack(
                                        children=[
                                            dmc.Title("Результаты поиска", order=3),
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
                                        style={"width": "100%", "min-height": "100px"},
                                        gap="xs",
                                    ),
                                    shadow="sm",
                                ),
                            ],
                            span=10,
                            className="adaptive-container",
                        ),
                        dmc.GridCol(span="auto", className="hided_element"),
                    ],
                    className="adaptive-block",
                ),
            ],
            pt=20,
            className="dmc-container",
        )

cont_search.getTypesAdditionFormatCallback()

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
    conn = db_connection.getConn()

    current_page -= 1

    PAGE_LIMIT = 20
    OFFSET = current_page * PAGE_LIMIT

    # check inputs and get results
    counter, query_results = cont_search.getSearchResults(conn, query, categories, types, limit=PAGE_LIMIT, offset=OFFSET)

    if counter == -1:
        return no_update, notif_empty_input, 1
    elif counter == -2:
        return "Ошибочка", no_update, 1
    elif counter == 0:
        return dmc.Title("По Вашему запросу результатов нет", order=5), no_update, 1
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
        service.logPrinter(
            request.remote_addr,
            "search",
            f'category {str(categories)} | type {str(types)} | query "{query}" | results {counter} | page {current_page} | time {round(time.time() - start_time, 3)}',
        )

        return (
            cont_search.formatSearchResults(
                query_results=query_results,
                mediafiles_links_format=mediafiles_links_format,
            ),
            result_notif,
            pages,
        )
