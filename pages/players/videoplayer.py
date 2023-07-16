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
import sqlite3

register_page(__name__, path="/players/videoplayer", icon="fa-solid:home")

def layout(v=None, **other_unknown_query_strings):
    if v!=None:
        conn = sqlite3.connect('bases/nstorage.sqlite3')
        c = conn.cursor()
        c.execute(f"SELECT * FROM youtube WHERE youtube_filehash = '{v}'")
        one_result = c.fetchone()
        channel = one_result[1]
        filename = one_result[2]
        name = '.'.join(filename.split('.')[:-1])
        link = f'http://192.168.3.33/storage/youtube/{channel}/{filename}'
        c.close()
        conn.close()
    else:
        channel = 'Saple'
        name = 'Big buck bunny'
        link = 'https://www.w3schools.com/html/mov_bbb.mp4'

    return dmc.Container(
        children=[
            dmc.Space(h=10),
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
                                volume=0.4
                            ),
                            dmc.Space(h=5),
                            html.H4(name, style={"width": "100%"}, id='player_videoname'),
                            dmc.Space(h=10),
                            dmc.Grid(
                                children=[
                                    dmc.Col(
                                        dmc.Center(
                                            dmc.Button(
                                                html.A(
                                                    channel,
                                                    href=f"/search?from_video_view=True&query={channel}",
                                                    style={"textDecoration": "none"},
                                                    id='player_channelLink'
                                                ),
                                                compact=True,
                                                variant="subtle",
                                                color="black",
                                            )
                                        ),
                                        span="content",
                                    ),
                                    dmc.Col(span="auto"),
                                    dmc.Col(
                                        dmc.Group(
                                            children=[
                                                dmc.Button(
                                                    "Скачать",
                                                    rightIcon=DashIconify(
                                                        icon="material-symbols:download-for-offline-outline-rounded",
                                                        width=20,
                                                    ),
                                                    compact=True,
                                                    variant="subtle",
                                                    color="black",
                                                    id='player_download'
                                                ),
                                                dmc.Button(
                                                    "Добавить в плейлист",
                                                    rightIcon=DashIconify(
                                                        icon="material-symbols:playlist-add-rounded",
                                                        width=20,
                                                    ),
                                                    compact=True,
                                                    variant="subtle",
                                                    color="black",
                                                    id='player_addToPlaylist'
                                                ),
                                                dmc.Button(
                                                    # "Сообщить",
                                                    leftIcon=DashIconify(
                                                        icon="material-symbols:flag-outline-rounded",
                                                        width=20,
                                                    ),
                                                    compact=True,
                                                    variant="subtle",
                                                    color="black",
                                                    id='player_report'
                                                ),
                                            ],
                                            spacing='xs'
                                        ),
                                        span="content",
                                    ),
                                ],
                                align="center",
                                style={"width": "100%"},
                            ),
                        ],
                        className="block-background mrrow",
                        width="auto",
                    ),
                    dbc.Col("А тут плейлист, и рекомендации следующих видео с автовоспроизведением (?)", className="block-background mrrow"),
                ],
                className="gx-3",
            ),
        ],
        pt=20,
        style={"paddingTop": 20},
        size="98%",
    )
