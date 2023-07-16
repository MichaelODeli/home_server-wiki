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
import dash_player as dp
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

register_page(__name__, path="/players/videoplayer", icon="fa-solid:home")

def layout(v=None, **other_unknown_query_strings):
    return dmc.Container(
        children=[
            dmc.Space(h=10),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dp.DashPlayer(
                                id="player",
                                url="https://www.w3schools.com/html/mov_bbb.mp4",
                                controls=True,
                                width="1200px",
                                className="video_container",
                            ),
                            dmc.Space(h=5),
                            html.H4("Big buck bunny "+str(v), style={"width": "100%"}, id='player_videoname'),
                            dmc.Space(h=10),
                            dmc.Grid(
                                children=[
                                    dmc.Col(
                                        dmc.Center(
                                            dmc.Button(
                                                html.A(
                                                    "Такой-то канал",
                                                    href="/",
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
