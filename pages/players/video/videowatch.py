from dash import (
    dcc,
    html,
    Input,
    Output,
    callback,
    register_page,
    State,
    no_update,
)
import dash_mantine_components as dmc
import dash_player as dp
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash_extensions import Purify
from flask import request
import sys
from controllers import service_controller as service
from controllers import db_connection, file_manager, cont_video, cont_search

register_page(__name__, path="/players/video/watch", icon="fa-solid:home")

video_id = ""
video_link = ""


def layout(l="n", v=None, **other_unknown_query_strings):
    service.logPrinter(request.remote_addr, "videoplayer", "page opened")
    if l == "n":
        return dmc.Container()

    global video_id
    global video_link
    video_id = v

    conn = db_connection.getConn()

    file_data = file_manager.getFileInfo(conn, file_id=video_id)

    if len(file_data) == 0:
        return dmc.Stack(
            [
                html.H5("Ошибка идентификатора видео. Попробуйте еще раз."),
            ],
            pt="30px",
            w="100%",
            align="center",
        )
    elif not file_data[0]["html_video_ready"]:
        return dmc.Stack(
            [
                html.H5("Неподдерживаемый файл."),
            ],
            pt="30px",
            w="100%",
            align="center",
        )
    else:
        file_data = file_data[0]

        video_name = ".".join(file_data["file_name"].split(".")[:-1])
        video_type = file_data["type_name"]
        video_type_id = file_data["type_id"]
        video_category = file_data["category_name"]
        video_category_id = file_data["category_id"]
        video_link = "http://" + file_data["file_fullway_forweb"]

    service.logPrinter(request.remote_addr, "videoplayer", f'v_id "{v}"')

    # video_link = "http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_60fps_normal.mp4"

    return html.Div(
        dmc.Container(
            children=[
                html.Div(id="notifications-container1"),
                dmc.Grid(
                    children=[
                        dmc.GridCol(
                            children=html.Div(
                                [
                                    dp.DashPlayer(
                                        id="player",
                                        url=video_link,
                                        controls=True,
                                        width="unset",
                                        height="max-content",
                                        className="video_container",
                                        volume=0.4,
                                        style={
                                            "width": "100% !important",
                                            "max-height": "80% !important",
                                        },
                                    ),
                                    dmc.Space(h=10),
                                    html.H4(
                                        video_name,
                                        style={"width": "100%"},
                                        id="player_videoname",
                                    ),
                                    dmc.Space(h=10),
                                    dmc.Grid(
                                        children=[
                                            dmc.GridCol(
                                                dmc.Tooltip(
                                                    label=f'Показать все видео с типа "{video_type}"',
                                                    position="top",
                                                    offset=3,
                                                    withArrow=True,
                                                    children=[
                                                        Purify(
                                                            f'<a href="/players/video/search?l=y&auto_search=y&category_id={video_category_id}&'
                                                            f'type_id={video_type_id}&from_video=y" '
                                                            f'class="btn btn-outline-primary btn-sm" role="button">{video_type}</a>'
                                                        )
                                                    ],
                                                ),
                                                span="content",
                                                w="max-content",
                                            ),
                                            dmc.GridCol(
                                                span="auto", className="adaptive-hide"
                                            ),
                                            dmc.GridCol(
                                                dmc.Group(
                                                    children=[
                                                        dmc.Tooltip(
                                                            label="Скачать видео",
                                                            position="bottom",
                                                            offset=3,
                                                            withArrow=True,
                                                            children=[
                                                                dbc.Button(
                                                                    Purify(
                                                                        '<i class="bi bi-download"></i>'
                                                                    ),
                                                                    size="sm",
                                                                    id="player_download",
                                                                    disabled=True,
                                                                    outline=True,
                                                                    className="btn btn-outline-primary",
                                                                ),
                                                            ],
                                                        ),
                                                        dmc.Tooltip(
                                                            label="Добавить в плейлист",
                                                            position="bottom",
                                                            offset=3,
                                                            withArrow=True,
                                                            children=[
                                                                dbc.Button(
                                                                    Purify(
                                                                        '<i class="bi bi-collection-play"></i>'
                                                                    ),
                                                                    size="sm",
                                                                    id="player_addtoplaylist",
                                                                    disabled=True,
                                                                    outline=True,
                                                                    className="btn btn-outline-primary",
                                                                ),
                                                            ],
                                                        ),
                                                        dmc.Tooltip(
                                                            label="Пожаловаться",
                                                            position="bottom",
                                                            offset=3,
                                                            withArrow=True,
                                                            children=[
                                                                dbc.Button(
                                                                    Purify(
                                                                        '<i class="bi bi-flag"></i>'
                                                                    ),
                                                                    size="sm",
                                                                    id="player_report",
                                                                    disabled=True,
                                                                    outline=True,
                                                                    className="btn btn-outline-primary",
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    gap="xs",
                                                ),
                                                span="content",
                                                w="max-content",
                                            ),
                                        ],
                                        align="center",
                                        style={"width": "100%"},
                                        # className="adaptive-block",
                                    ),
                                ],
                                className="block-background border",
                            ),
                            className="columns-margin adaptive-width p-0",
                            span="auto",
                            # mah='80dvh'
                        ),
                        dmc.GridCol(
                            children=[
                                cont_video.createVideoMiniaturesContainer(
                                    children=[
                                        cont_video.createVideoMiniatureContainer(
                                            href=f"/players/video/watch?v={video['file_id']}&l=y",
                                            video_title=cont_search.stringHider(
                                                ".".join(
                                                    video["file_name"].split(".")[:-1]
                                                )
                                            ),
                                            videotype_name=video["type_name"],
                                            video_duration=video["video_duration"],
                                        )
                                        for video in cont_video.getRandomVideos(conn, type_id=video_type_id, counter=6)
                                    ],
                                )
                            ],
                            className="block-background border columns-margin adaptive-width",
                            span=3,
                            style={"overflow": "auto", "height": "89dvh"},
                        ),
                    ],
                    # className="gx-3",
                    gutter="xl",
                    className="adaptive-block",
                ),
                dcc.Download(id="download-video"),
            ],
            pt=20,
            className="dmc-container",
            size="98%",
        )
    )


@callback(
    [
        Output("download-video", "data"),
        Output("notifications-container1", "children"),
    ],
    Input("player_download", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    global video_link
    service.logPrinter(
        request.remote_addr, "videoplayer", f"download triggered | {video_link}"
    )
    notif_bad = dmc.Notification(
        title="Ошибка при загрузке файла",
        id="simple-notify",
        action="show",
        message="Попробуйте попытку позже. ",
        color="red",
        icon=DashIconify(icon="ic:outline-error"),
    )
    notif_cool = dmc.Notification(
        title="Начинаю загрузку...",
        id="simple-notify",
        action="show",
        message="Подождите немного, начинаю скачивание видео.",
        color="green",
        icon=DashIconify(icon="ep:success-filled"),
    )

    if sys.platform == "linux" or sys.platform == "linux2":
        link_l = video_link.replace("http://localhost", "/home/michael/server-side")
        return None, notif_bad
    elif sys.platform == "win32":
        link_l = video_link.replace("http://localhost/storage", "Z:")
    else:
        raise OSError("Unsupported OS")

    try:
        return dcc.send_file(video_link), notif_cool
    except OSError:
        return None, notif_bad
