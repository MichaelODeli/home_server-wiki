from dash import register_page, html
from controllers import service_controller as service
from flask import request
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_extensions import Purify
from controllers import cont_video

register_page(__name__, path="/players/video", icon="fa-solid:home")


def layout(l="n", **other_unknown_query_strings):
    service.log_printer(request.remote_addr, "videomain", "page opened")
    if l == "n":
        return dmc.Container()
    else:

        return dmc.Stack(
            pt="20px",
            gap="xs",
            children=[
                cont_video.video_search_bar(page='main'),
                cont_video.video_miniatures_container(
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
                    * 6
                    * 5,
                ),
            ],
        )
