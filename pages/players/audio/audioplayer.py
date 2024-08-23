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
import dash_player

register_page(__name__, path="/players/audio", icon="fa-solid:home")


def layout(l="n", selected_playlist_name="Любимые треки", **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        service.logPrinter(request.remote_addr, "audioplayer", "page opened")
        df = pd.read_csv(
            "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
        )
        return dmc.Container(
            children=[
                dash_player.DashPlayer(
                    id="audio-player",
                    url="https://www.youtube.com/watch?v=4xnsmyI5KMQ&t=1s",
                    width="0",
                    height="0",
                    style={"display": "none"},
                    intervalCurrentTime=500,
                    volume=20
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dmc.Stack(
                                    [
                                        cont_a.audioLeftColumn(source="col"),
                                    ],
                                    className="block-background",
                                )
                            ],
                            className="hided_column",
                            width=3,
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    style={"height": "500px"},
                                    className="block-background-audio",
                                    children=[
                                        dmc.Stack(
                                            [
                                                html.H4(
                                                    selected_playlist_name,
                                                    style={
                                                        "margin-bottom": "0 !important"
                                                    },
                                                ),
                                                dmc.Divider(color="--bs-blue"),
                                                html.Div(
                                                    html.Table(cont_a.createTable(df), style={"width": "100%"},),
                                                    className="table-wrapper",
                                                ),
                                            ]
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
                cont_a.getDrawer(),
            ],
            pt=20,
            className="dmc-container adaptive-container",
        )


@callback(
    Output("drawer-albums", "opened"),
    Input("open-drawer-albums", "n_clicks"),
    prevent_initial_call=True,
)
def drawerWithAlbums(n_clicks):
    return True


@callback(
    [
        Output("audio-player", "playing"),
        Output("playpause-icon", 'icon')
    ],
    Input("control-playpause", "n_clicks"),
    State("audio-player", "playing"),
    prevent_initial_call=True,
)
def playerPlayPause(n_clicks, playing):
    if not playing == True:
        icon = 'material-symbols:pause'
    else:
        icon = 'material-symbols:play-arrow'
    return not playing, icon


@callback(
    [
        Output("audio-player", "loop"),
        Output("loop-icon", 'icon')
    ],
    Input("control-repeat", "n_clicks"),
    State("audio-player", "loop"),
    prevent_initial_call=True,
)
def playerLoop(n_clicks, loop):
    if not loop == True:
        icon = 'material-symbols:repeat-on'
    else:
        icon = 'material-symbols:repeat'
    return not loop, icon


@callback(
    [
        Output("audio-player", "muted"),
        Output("muted-icon", 'icon')
    ],
    Input("volume-muted", "n_clicks"),
    State("audio-player", "muted"),
    prevent_initial_call=True,
)
def playerDisableSound(n_clicks, muted):
    if not muted == True:
        icon = 'material-symbols:volume-off'
    else:
        icon = 'material-symbols:volume-up'
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
        Output("audio-full-time", "children")
    ],
    Input("audio-player", "currentTime"),
    State("audio-player", "duration"),
    prevent_initial_call=True,
)
def playerVolume(currentTime, duration):
    currentTime = int(currentTime) if currentTime != None else 0
    duration = int(duration) if duration != None else 0

    return currentTime, duration, cont_m.getDuration(currentTime), cont_m.getDuration(duration)
