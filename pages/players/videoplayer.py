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
import sqlite3
import dash_mantine_components as dmc
import dash_player as dp
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash_extensions import Purify
from flask import request
from datetime import datetime
from utils import sql_traceback_generator

register_page(__name__, path="/players/videoplayer", icon="fa-solid:home")

link = ""


def get_video_card(video_title, video_length, video_link):
    return html.A(
        [
            dmc.Card(
                children=[
                    dmc.CardSection(
                        dmc.Image(
                            src="/assets/image-not-found.jpg",
                            height=120,
                        )
                    ),
                    dmc.Group(
                        [
                            dmc.Text(str(video_title), weight=500),
                            dbc.Badge(
                                str(video_length),
                                text_color="primary",
                                className="border me-1",
                                color="white",
                            ),
                        ],
                        position="apart",
                        mt="md",
                        mb="xs",
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": "auto"},  # prev: 350px
            )
        ],
        href=video_link,
    )


def layout(l="n", v=None, v_type="youtube", **other_unknown_query_strings):
    if l == "n":
        return dmc.Container()
    global link
    # server_link = '192.168.3.33'
    server_link = request.base_url.replace(":81", "").split("/")[2]
    if v != None:
        try:
            conn = sqlite3.connect("bases/nstorage.sqlite3")
            c = conn.cursor()
            c.execute(f"SELECT * FROM {v_type} WHERE {v_type}_filehash = '{v}'")
            one_result = c.fetchone()
            channel = one_result[1]
            filename = one_result[2]
            name = ".".join(filename.split(".")[:-1])
            link = f"http://{server_link}/storage/{v_type}/{channel}/{filename}"
            c.close()
            conn.close()
        except sqlite3.Error as er:
            err_cont = sql_traceback_generator.gen(er)
            return err_cont
    else:
        v = "default_video"
        channel = "Blender"
        name = "Big buck bunny"
        link = "https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_320x180.mp4"

    now = datetime.now().strftime("%d/%b/%Y %H:%M:%S") 
    print(
        f'{request.remote_addr} - - [{now}] | videoview | v_id "{v}" | v_type "{v_type}"'
    )
    return dmc.Container(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dp.DashPlayer(
                                id="player",
                                url=link,
                                controls=True,
                                width="1200px",
                                className="video_container",
                                volume=0.4,
                            ),
                            dmc.Space(h=10),
                            html.H4(
                                name, style={"width": "100%"}, id="player_videoname"
                            ),
                            dmc.Space(h=10),
                            dmc.Grid(
                                children=[
                                    dmc.Col(
                                        dmc.Center(
                                            [
                                                dmc.Tooltip(
                                                    label=f'Перейти на канал "{channel}"',
                                                    position="bottom",
                                                    offset=3,
                                                    withArrow=True,
                                                    children=[
                                                        Purify(
                                                            f'<a href="/search?l=y&from_video_view=True&query={channel}" class="btn btn-outline-primary btn-sm" role="button">{channel}</a>'
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        span="content",
                                    ),
                                    dmc.Col(span="auto"),
                                    dmc.Col(
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
                                                        ),
                                                    ]
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
                                                        ),
                                                    ]
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
                                                        ),
                                                    ]
                                                ),
                                                
                                                
                                            ],
                                            spacing="xs",
                                        ),
                                        span="content",
                                    ),
                                ],
                                align="center",
                                style={"width": "100%"},
                            ),
                        ],
                        className="block-background columns-margin video-column",
                        width="auto",
                    ),
                    dbc.Col(
                        children=[
                            html.H5("Смотрите также:"),
                            dbc.ButtonGroup(
                                [
                                    dbc.Button(
                                        "Рекомендации", disabled=True, outline=True
                                    ),
                                    dbc.Button(f"Канал: {channel}"),
                                    dbc.Button("Похожие", disabled=True, outline=True),
                                ],
                                style={"width": "100%"},
                            ),
                            dmc.Space(h=7),
                            get_video_card(
                                "Sample video 1", "00:50", "https://example.com"
                            ),
                            dmc.Space(h=7),
                            get_video_card(
                                "Sample video 2", "01:50", "https://example.com"
                            ),
                            dmc.Space(h=7),
                            get_video_card(
                                "Sample video 3", "02:50", "https://example.com"
                            ),
                            dmc.Space(h=7),
                            get_video_card(
                                "Sample video 4", "03:50", "https://example.com"
                            ),
                            dmc.Space(h=7),
                            get_video_card(
                                "Sample video 5", "1:04:50", "https://example.com"
                            ),
                        ],
                        className="block-background columns-margin overflow-column",
                    ),
                ],
                className="gx-3",
            ),
        ],
        pt=20,
        style={"paddingTop": 20},
        size="98%",
    )
