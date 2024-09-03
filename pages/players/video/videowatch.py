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
    video_type_id = None

    if len(file_data) == 0:
        videoplayer_children = dmc.Stack(
            [
                dmc.Title("Ошибка идентификатора видео. Попробуйте еще раз.", order=4),
                html.A(
                    "Перейти на главную страницу",
                    href="/players/video?l=y",
                    className="btn btn-outline-primary btn-sm",
                    role="button",
                ),
            ],
            w="100%",
            h="100%",
            align="center",
        )
        elements_justify = "center"

    elif not file_data[0]["html_video_ready"]:
        videoplayer_children = dmc.Stack(
            [
                dmc.Title("Неподдерживаемый файл.", order=4),
                html.A(
                    "Перейти на главную страницу",
                    href="/players/video?l=y",
                    className="btn btn-outline-primary btn-sm",
                    role="button",
                ),
            ],
            w="100%",
            h="100%",
            align="center",
        )
        elements_justify = "center"

    else:
        elements_justify = None
        file_data = file_data[0]

        video_name = ".".join(file_data["file_name"].split(".")[:-1])
        video_type = file_data["type_name"]
        video_type_id = file_data["type_id"]
        video_category = file_data["category_name"]
        video_category_id = file_data["category_id"]
        video_link = "http://" + file_data["file_fullway_forweb"]

        videoplayer_children = [
            dmc.Space(),
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
                },
            ),
            dmc.Space(),
            dmc.Title(
                video_name, style={"width": "100%"}, id="player_videoname", order=3
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.Tooltip(
                            label=f'Показать все видео "{video_type}"',
                            position="top",
                            offset=3,
                            withArrow=True,
                            children=[
                                service.dmcButtonLink(
                                    video_type,
                                    href=cont_video.getSearchLink(
                                        video_category_id,
                                        video_type_id,
                                    )
                                )
                            ],
                        ),
                        span="content",
                        w="max-content",
                    ),
                    dmc.GridCol(span="auto", className="adaptive-hide"),
                    dmc.GridCol(
                        dmc.Group(
                            children=[
                                dmc.Tooltip(
                                    label="Скачать видео",
                                    position="bottom",
                                    offset=3,
                                    withArrow=True,
                                    children=[
                                        dmc.Button(
                                            Purify('<i class="bi bi-download"></i>'),
                                            id="player_download",
                                            variant="outline",
                                        ),
                                    ],
                                ),
                                dmc.Tooltip(
                                    label="Добавить в плейлист",
                                    position="bottom",
                                    offset=3,
                                    withArrow=True,
                                    children=[
                                        dmc.Button(
                                            Purify(
                                                '<i class="bi bi-collection-play"></i>'
                                            ),
                                            id="player_addtoplaylist",
                                            disabled=True,
                                            variant="outline",
                                        ),
                                    ],
                                ),
                                dmc.Tooltip(
                                    label="Пожаловаться",
                                    position="bottom",
                                    offset=3,
                                    withArrow=True,
                                    children=[
                                        dmc.Button(
                                            Purify('<i class="bi bi-flag"></i>'),
                                            id="player_report",
                                            disabled=True,
                                            variant="outline",
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
        ]

    service.logPrinter(request.remote_addr, "videoplayer", f'v_id "{v}"')

    # video_link = "http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_60fps_normal.mp4"

    return html.Div(
        dmc.Container(
            children=[
                html.Div(id="notifications-container1"),
                dmc.Grid(
                    children=[
                        dmc.GridCol(
                            children=dmc.Stack(
                                videoplayer_children,
                                className="mih-100",
                                justify=elements_justify,
                                # gap='xs'
                            ),
                            className="columns-margin adaptive-width p-0",
                            span="auto",
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
                                            date=service.get_date_difference(
                                                video["created_at"]
                                            ),
                                            category_id=video["category_id"],
                                            type_id=video["type_id"],
                                        )
                                        for video in cont_video.getRandomVideos(
                                            conn, type_id=video_type_id, counter=6
                                        )
                                    ],
                                )
                            ],
                            className="columns-margin adaptive-width",
                            span=3,
                        ),
                    ],
                    # className="gx-3",
                    gutter="xl",
                    className="adaptive-block",
                ),
            ],
            pt=20,
            className="dmc-container",
            size="98%",
        )
    )


@callback(
    [
        Output("notifications-container1", "children"),
    ],
    Input("player_download", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    notif = dmc.Notification(
        title="Информация о загрузке видео",
        id="simple-notify",
        action="show",
        message="Для загрузки видео нажмите на три точки в плеере - 'Скачать'",
        color="green",
        icon=service.getIcon("ep:success-filled", background=False),
    )

    return (notif,)
