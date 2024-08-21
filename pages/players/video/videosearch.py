from dash import register_page, html, callback, Input, Output, State, no_update
from controllers import service_controller as service
from flask import request
import dash_mantine_components as dmc
from controllers import cont_video, cont_search, db_connection, file_manager
from dash.exceptions import PreventUpdate

register_page(__name__, path="/players/video/search", icon="fa-solid:home")


def layout(
    l="n",
    query="",
    category_id=[],
    type_id=[],
    auto_search="n",
    **other_unknown_query_strings,
):
    service.logPrinter(request.remote_addr, "videosearch", "page opened")
    if l == "n":
        return dmc.Container()
    else:
        conn = db_connection.getConn()

        category_id, type_id = cont_search.formatCategoryType(category_id, type_id)

        category_select_data = cont_search.getCategoriesForMultiSelect(conn, video=True)


        if auto_search != "n" and (query != "" or category_id != []):
            search_clicks = 1
        else:
            search_clicks = 0

        return dmc.Stack(
            id="dummy-1",
            pt="20px",
            gap="xs",
            children=[
                cont_video.createVideoSearchBar(
                    page="search",
                    input_value=query,
                    additional_children=[
                        cont_search.getSearchAccordion(
                            category_id, type_id, category_select_data, from_video=True
                        )
                    ],
                    search_clicks=search_clicks,
                ),
                html.Div(id="search_results_video"),
                html.Center(
                    dmc.Pagination(
                        total=1,
                        value=1,
                        siblings=1,
                        withControls=True,
                        withEdges=True,
                        id="search_pagination_video",
                    ),
                    style={"width": "100%"},
                    className="py-3",
                ),
            ],
        )


cont_search.getTypesAdditionFormatCallback(from_video=True)


@callback(
    Output("search_results_video", "children"),
    Output("search_pagination_video", "total"),
    Input("search_pagination_video", "value"),
    Input("n_search_button_video", "n_clicks"),
    State("n_search_in_category_video", "value"),
    State("n_search_in_types_video", "value"),
    State("n_search_query_video", "value"),
)
def getVideoSearchResults(current_page, n_clicks, categories, types, query):
    if n_clicks == 0:
        return html.Center([html.H5("Пустой поисковый запрос. Повторите снова.")]), 1
    else:
        conn = db_connection.getConn()
        current_page -= 1

        page_limit = cont_search.PAGE_LIMIT
        offset = current_page * page_limit

        counter, query_results = cont_search.getSearchResults(
            conn,
            query,
            categories,
            types,
            limit=page_limit,
            offset=offset,
            from_video=True,
        )

        if counter == -1:
            return no_update, 1
        elif counter == -2:
            return "Ошибочка", 1
        elif counter == 0:
            return html.Center(html.H5("По Вашему запросу результатов нет")), 1
        else:
            pages = (
                int(counter / page_limit) + 1
                if counter % page_limit != 0
                else counter / page_limit
            )

            return (
                cont_video.createVideoMiniaturesContainer(
                    children=[
                        cont_video.createVideoMiniatureContainer(
                            href=f"/players/video/watch?v={result['file_id']}&l=y",
                            video_title=cont_search.stringHider(
                                ".".join(result["file_name"].split(".")[:-1])
                            ),
                            videotype_name=cont_search.stringHider(result["type_name"]),
                            video_duration=result["video_duration"]
                        )
                        for result in query_results
                    ]
                ),
                pages,
            )
