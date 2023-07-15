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

layout = dmc.Container(
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
                        html.H4("Big buck bunny", style={"width": "100%"}),
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
                dbc.Col("Nice!", className="block-background mrrow"),
            ],
            className="gx-3",
        ),
    ],
    pt=20,
    style={"paddingTop": 20},
    size="98%",
)
