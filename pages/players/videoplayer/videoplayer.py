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
import sqlite3
import dash_mantine_components as dmc
import dash_player as dp
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash_extensions import Purify
from flask import request
import sys
from controllers import service_controller as service
from controllers import db_connection, file_manager

register_page(__name__, path="/players/videoplayer", icon="fa-solid:home") 

video_id = ""
video_link = ""


def layout(l="n", v=None, v_type="youtube", **other_unknown_query_strings):
    service.log_printer(request.remote_addr, "videoplayer", "page opened")
    if l == "n":
        return dmc.Container()

    global video_id
    global video_link
    video_id = v

    conn = db_connection.get_conn()

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
                html.H5("Неподдерживаемый файл"),
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

    service.log_printer(request.remote_addr, "videoplayer", f'v_id "{v}"')

    return html.Div(
        dmc.Container(
            children=[
                html.Div(id="notifications-container1"),
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                dp.DashPlayer(
                                    id="player",
                                    url=video_link,
                                    controls=True,
                                    width="1200px",
                                    className="video_container",
                                    volume=0.4,
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
                                            dmc.Center(
                                                [
                                                    dmc.Tooltip(
                                                        label=f'Показать все видео с типа "{video_type}"',
                                                        position="top",
                                                        offset=3,
                                                        withArrow=True,
                                                        children=[
                                                            Purify(
                                                                f'<a href="/search?l=y&auto_search=y&category_id={video_category_id}&'
                                                                f'type_id={video_type_id}" '
                                                                f'class="btn btn-outline-primary btn-sm" role="button">{video_type}</a>'
                                                            )
                                                        ],
                                                    ),
                                                ]
                                            ),
                                            span="content",
                                        ),
                                        dmc.GridCol(span="auto"),
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
                                        ),
                                    ],
                                    align="center",
                                    style={"width": "100%"},
                                ),
                            ],
                            className="block-background columns-margin video-column border",
                            width="auto",
                        ),
                        dbc.Col(
                            children=[
                                # html.H5("Смотрите также:"),
                                # dmc.Stack(h=10),
                                # dbc.ButtonGroup(
                                #     [
                                #         dbc.Button(
                                #             "Рекомендации",
                                #             # disabled=True,
                                #             outline=True,
                                #             color="primary",
                                #             id="video-button-recommended",
                                #             n_clicks=0,
                                #             size="sm",
                                #         ),
                                #         dbc.Button(
                                #             f"Тип: {video_type}",
                                #             active=True,
                                #             outline=True,
                                #             color="primary",
                                #             id="video-button-video_type",
                                #             n_clicks=0,
                                #             size="sm",
                                #         ),
                                #         dbc.Button(
                                #             "Похожие",
                                #             # disabled=True,
                                #             outline=True,
                                #             color="primary",
                                #             id="video-button-same",
                                #             n_clicks=0,
                                #             size="sm",
                                #         ),
                                #     ],
                                #     style={"width": "100%"},
                                # ),
                                # dmc.Space(h=10),
                                # html.Div(
                                #     [
                                #         cont_v.get_video_card(
                                #             "Sample video 1",
                                #             "00:50",
                                #             "https://example.com",
                                #         ),
                                #         dmc.Space(h=7),
                                #         cont_v.get_video_card(
                                #             "Sample video 2",
                                #             "01:50",
                                #             "https://example.com",
                                #         ),
                                #         dmc.Space(h=7),
                                #         cont_v.get_video_card(
                                #             "Sample video 3",
                                #             "02:50",
                                #             "https://example.com",
                                #         ),
                                #         dmc.Space(h=7),
                                #         cont_v.get_video_card(
                                #             "Sample video 4",
                                #             "03:50",
                                #             "https://example.com",
                                #         ),
                                #     ],
                                #     id="recommended-videos-tab",
                                # ),
                            ],
                            className="block-background columns-margin overflow-column border",
                        ),
                    ],
                    className="gx-3",
                ),
                dcc.Download(id="download-video"),
            ],
            pt=20,
            # style={"paddingTop": 20},
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
    service.log_printer(
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
        link_l = video_link.replace('http://localhost', '/home/michael/server-side')
        return None, notif_bad
    elif sys.platform == "win32":
        link_l = video_link.replace("http://localhost/storage", "Z:")
    else:
        raise OSError("Unsupported OS")

    try:
        return dcc.send_file(video_link), notif_cool
    except OSError:
        return None, notif_bad


@callback(
    [
        Output("video-button-recommended", "active"),
        Output("video-button-video_type", "active"),
        Output("video-button-same", "active"),
        Output("video-button-recommended", "n_clicks"),
        Output("video-button-video_type", "n_clicks"),
        Output("video-button-same", "n_clicks"),
        # Output('recommended-videos-tab', 'children')
    ],
    [
        Input("video-button-recommended", "n_clicks"),
        Input("video-button-video_type", "n_clicks"),
        Input("video-button-same", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def videos_tab_recommended(rec_c, chan_c, same_c):
    # if clicked - current n_clicks value will be bigger than previous
    if rec_c != 0:
        content = html.Div()
    elif chan_c != 0:
        content = html.Div()
    elif same_c != 0:
        content = html.Div()
    else:
        raise ValueError

    vars_list = [rec_c, chan_c, same_c]

    return [False if element == 0 else True for element in vars_list] + [0] * 3
