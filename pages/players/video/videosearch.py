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
    **other_unknown_query_strings
):
    service.log_printer(request.remote_addr, "videosearch", "page opened")
    if l == "n":
        return dmc.Container()
    else:
        conn = db_connection.get_conn()

        category_id, type_id = cont_search.format_category_type(category_id, type_id)

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
            if i["main_mime_type_id"] == 9
        ]

        if auto_search != "n" and (query != "" or category_id != []):
            search_clicks = 1
        else:
            search_clicks = 0

        return dmc.Stack(
            id="dummy-1",
            pt="20px",
            gap="xs",
            children=[
                cont_video.video_search_bar(
                    page="search",
                    input_value=query,
                    additional_children=[
                        cont_search.search_accordion(
                            category_id, type_id, category_select_data, from_video=True
                        )
                    ],
                    search_clicks=search_clicks,
                ),
                html.Div(id="search_results_video"),
            ],
        )


cont_search.get_types_addition_format_callback(from_video=True)


@callback(
    Output("search_results_video", "children"),
    Input("n_search_button_video", "n_clicks"),
    State("n_search_in_category_video", "value"),
    State("n_search_in_types_video", "value"),
    State("n_search_query_video", "value"),
)
def get_video_search_results(n_clicks, categories, types, query):
    if n_clicks == 0:
        return html.Center([html.H5("Пустой поисковый запрос. Повторите снова.")])
    else:
        print(categories, types, query)
        return cont_video.video_miniatures_container(
            children=[
                cont_video.create_video_container(
                    href="/players/video/watch?v=3edbac2814a1b990acc291ed86278398d61bdcb0409d8ec64ad8a6236f4feadc&l=y",
                    img_video="/assets/img/image-not-found.jpg",
                    img_channel="/assets/img/image-not-found.jpg",
                    video_title="Случайное такси E01_AniDUB",
                    videotype_name="OddTaxi",
                    views="0 просмотров",
                    date="сегодня",
                )
            ]
            * 3
        )
