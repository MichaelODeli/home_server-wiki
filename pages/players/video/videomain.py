from dash import register_page, html
from controllers import service_controller as service
from flask import request
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_extensions import Purify
from controllers import cont_video, db_connection, cont_search

register_page(__name__, path="/players/video", icon="fa-solid:home")


def layout(l="n", **other_unknown_query_strings):
    service.logPrinter(request.remote_addr, "videomain", "page opened")
    if l == "n":
        return dmc.Container()
    else:
        conn = db_connection.getConn()

        return dmc.Stack(
            pt="20px",
            gap="xs",
            children=[
                # cont_video.createVideoSearchBar(page="main"),
                cont_video.createVideoMiniaturesContainer(
                    children=[
                        cont_video.createVideoMiniatureContainer(
                            href=f"/players/video/watch?v={video['file_id']}&l=y",
                            video_title=cont_search.stringHider(
                                ".".join(video["file_name"].split(".")[:-1])
                            ),
                            videotype_name=video["type_name"],
                            video_duration=video["video_duration"],
                            date=service.get_date_difference(video["created_at"]),
                            category_id=video["category_id"],
                            type_id=video["type_id"],
                        )
                        for video in cont_video.getRandomVideos(conn)
                    ],
                ),
            ],
        )
