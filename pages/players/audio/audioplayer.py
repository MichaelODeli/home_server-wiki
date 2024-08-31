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
    ALL,
    ctx,
)
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_extensions import Purify
from dash_iconify import DashIconify
from flask import request
from datetime import datetime
import pandas as pd
from controllers import cont_audioplayer as cont_a
from controllers import service_controller as service
from controllers import cont_search as cont_s
from controllers import cont_media as cont_m
from controllers import db_connection, file_manager
import dash_player

register_page(__name__, path="/players/audio", icon="fa-solid:home")


def layout(l="n", selected_playlist_name="Главная", **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        service.logPrinter(request.remote_addr, "audioplayer", "page opened")

        conn = db_connection.getConn()

        return dmc.Container(
            children=[
                dash_player.DashPlayer(
                    id="audio-player",
                    url="https://www.youtube.com/watch?v=4xnsmyI5KMQ&t=1s",
                    width="0",
                    height="0",
                    style={"display": "none"},
                    intervalCurrentTime=500,
                    volume=20,
                ),
                dmc.Space(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dmc.Stack(
                                    [
                                        cont_a.audioLeftColumn(source="col", conn=conn),
                                    ],
                                )
                            ],
                            className="hided_column",
                            width=3,
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    style={"height": "500px"},
                                    children=[
                                        dmc.Stack(
                                            [
                                                html.H3(
                                                    selected_playlist_name,
                                                    style={
                                                        "margin-bottom": "0 !important"
                                                    },
                                                    id="audioplayer-playlist-name",
                                                ),
                                                dmc.Space(),
                                                dmc.Group(
                                                    id="audio-playlist-description"
                                                ),
                                                html.Div(
                                                    dmc.Table(
                                                        # hover=True,
                                                        children=[
                                                            dmc.TableThead(
                                                                dmc.TableTr(
                                                                    [
                                                                        dmc.TableTh(
                                                                            className="min-column-width px-2",
                                                                        ),
                                                                        dmc.TableTh(
                                                                            className="min-column-width px-2",
                                                                        ),
                                                                        dmc.TableTh(
                                                                            "Название",
                                                                            className="px-2",
                                                                        ),
                                                                        dmc.TableTh(
                                                                            "Альбом",
                                                                            className="px-2 adaptive-hide",
                                                                        ),
                                                                        dmc.TableTh(
                                                                            "Загружено",
                                                                            className="min-column-width px-2 adaptive-hide",
                                                                        ),
                                                                        dmc.TableTh(
                                                                            "🕑",
                                                                            className="min-column-width px-2 center-content",
                                                                        ),
                                                                    ]
                                                                ),
                                                                className="sticky-th",
                                                            ),
                                                            dmc.TableTbody(
                                                                className="audio-content",
                                                                children=[
                                                                    dmc.TableTr(
                                                                        [
                                                                            dmc.TableTd(
                                                                                dmc.ActionIcon(
                                                                                    radius="xl",
                                                                                    children=DashIconify(
                                                                                        icon="mdi:play"
                                                                                    ),
                                                                                ),
                                                                                className="min-column-width p-2",
                                                                            ),
                                                                            dmc.TableTd(
                                                                                dmc.Avatar(
                                                                                    radius="sm"
                                                                                ),
                                                                                className="min-column-width p-2",
                                                                            ),
                                                                            dmc.TableTd(
                                                                                dmc.Stack(
                                                                                    [
                                                                                        dmc.Text(
                                                                                            "Название трека"
                                                                                        ),
                                                                                        html.A(
                                                                                            "Исполнитель",
                                                                                            className="audio-link w-content",
                                                                                            href="#",
                                                                                        ),
                                                                                    ],
                                                                                    gap=0,
                                                                                ),
                                                                                className="p-2",
                                                                            ),
                                                                            dmc.TableTd(
                                                                                html.A(
                                                                                    "Альбом",
                                                                                    className="audio-link w-content",
                                                                                    href="#",
                                                                                ),
                                                                                className="p-2 adaptive-hide",
                                                                            ),
                                                                            dmc.TableTd(
                                                                                "Вчера",
                                                                                className="min-column-width p-2 adaptive-hide",
                                                                            ),
                                                                            dmc.TableTd(
                                                                                "3:15",
                                                                                className="min-column-width p-2",
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                                * 20,
                                                            ),
                                                        ],
                                                        className="w-100 no-box-shadow",
                                                        highlightOnHover=True,
                                                    ),
                                                    className="w-100 overflow-auto pb-5",
                                                    style={"max-height": "78dvh"},
                                                ),
                                            ],
                                            gap="xs",
                                        )
                                    ],
                                )
                            ]
                        ),
                    ]
                ),
                dmc.Affix(
                    children=[cont_a.floatPlayer()],
                    style={"width": "100%"},
                ),
                cont_a.getDrawer(conn),
            ],
            pt=20,
            className="dmc-container adaptive-container",
            id="dummy-3",
            mah="90dvh",
        )


@callback(
    Output("drawer-albums", "opened", allow_duplicate=True),
    Input("open-drawer-albums", "n_clicks"),
    prevent_initial_call=True,
)
def drawerWithAlbums(n_clicks):
    return True


@callback(
    [Output("audio-player", "playing"), Output("playpause-icon", "icon")],
    Input("control-playpause", "n_clicks"),
    State("audio-player", "playing"),
    prevent_initial_call=True,
)
def playerPlayPause(n_clicks, playing):
    if not playing == True:
        icon = "material-symbols:pause"
    else:
        icon = "material-symbols:play-arrow"
    return not playing, icon


@callback(
    [Output("audio-player", "loop"), Output("loop-icon", "icon")],
    Input("control-repeat", "n_clicks"),
    State("audio-player", "loop"),
    prevent_initial_call=True,
)
def playerLoop(n_clicks, loop):
    if not loop == True:
        icon = "material-symbols:repeat-on"
    else:
        icon = "material-symbols:repeat"
    return not loop, icon


@callback(
    [Output("audio-player", "muted"), Output("muted-icon", "icon")],
    Input("volume-muted", "n_clicks"),
    State("audio-player", "muted"),
    prevent_initial_call=True,
)
def playerDisableSound(n_clicks, muted):
    if not muted == True:
        icon = "material-symbols:volume-off"
    else:
        icon = "material-symbols:volume-up"
    return not muted, icon


@callback(
    Output("audio-player", "volume"),
    Input("volume-slider", "value"),
    State("audio-player", "volume"),
    # prevent_initial_call=True,
)
def playerVolumeSlider(volume_value, current_vol):
    return volume_value / 100


@callback(
    [
        Output("progress-slider", "value"),
        Output("progress-slider", "max"),
        Output("audio-current-time", "children"),
        Output("audio-full-time", "children"),
    ],
    Input("audio-player", "currentTime"),
    State("audio-player", "duration"),
    prevent_initial_call=True,
)
def playerVolume(currentTime, duration):
    currentTime = int(currentTime) if currentTime != None else 0
    duration = int(duration) if duration != None else 0

    return (
        currentTime,
        duration,
        cont_m.getDuration(currentTime),
        cont_m.getDuration(duration),
    )


@callback(
    Output({"type": "audio-playlist-btn-col", "id": ALL}, "n_clicks"),
    Output({"type": "audio-playlist-btn-drawer", "id": ALL}, "n_clicks"),
    Output("audioplayer-playlist-name", "children"),
    Output("drawer-albums", "opened"),
    Output("audio-playlist-description", "children"),
    Input({"type": "audio-playlist-btn-col", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-drawer", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-home", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-search", "id": ALL}, "n_clicks"),
    State({"type": "audio-playlist-btn-drawer", "id": ALL}, "id"),
    State("drawer-albums", "opened"),
    prevent_initial_call=True,
)
def buttonsVerify(
    n_clicks_col, n_clicks_drawer, n_clicks_home, n_clicks_search, button_ids, opened
):
    types_ids = [i["id"] for i in button_ids]

    description = None
    if ctx.triggered_id["type"] == "audio-playlist-btn-home":
        page_name = "Главная"
    elif ctx.triggered_id["type"] == "audio-playlist-btn-search":
        page_name = "Поиск"
    else:
        description = [
            dmc.Badge("1250 треков", variant="light"),
            dmc.Badge("500 минут", variant="light"),
        ]

        if ctx.triggered_id["type"] == "audio-playlist-btn-col":
            selected_type = types_ids[n_clicks_col.index(1)]
        elif ctx.triggered_id["type"] == "audio-playlist-btn-drawer":
            selected_type = types_ids[n_clicks_drawer.index(1)]
        else:
            raise PreventUpdate

        conn = db_connection.getConn()
        page_name = cont_a.getAudioTypes(conn, type_id=selected_type)[0]["type_name"]

    return (
        [None] * len(n_clicks_col),
        [None] * len(n_clicks_drawer),
        page_name,
        False,
        description,
    )
