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
from controllers import bl_search as bl_s
import dash_player

register_page(__name__, path="/players/audioplayer", icon="fa-solid:home")


def layout(l="n", selected_playlist_name="Любимые треки", **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        # now = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        # print(f"{request.remote_addr} - - [{now}] | audioplayer page")
        service.log_printer(request.remote_addr, "audioplayer", "page opened")
        df = pd.read_csv(
            "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
        )
        return dmc.Container(
            children=[
                dash_player.DashPlayer(
                    id="player",
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
                                        cont_a.audio_leftcollumn(source="col"),
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
                                                    dmc.Table(cont_a.create_table(df)),
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
                    children=[cont_a.float_player()],
                    style={"width": "100%"},
                ),
                cont_a.get_drawer(),
            ],
            pt=20,
            className="dmc-container adaptive-container",
        )


@callback(
    Output("drawer-albums", "opened"),
    Input("open-drawer-albums", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_with_albums(n_clicks):
    return True


@callback(
    [
        Output("player", "playing"),
        Output("playpause-icon", 'icon')
    ],
    Input("control-playpause", "n_clicks"),
    State("player", "playing"),
    prevent_initial_call=True,
)
def player_playpause(n_clicks, playing):
    if not playing == True:
        icon = 'material-symbols:pause'
    else:
        icon = 'material-symbols:play-arrow'
    return not playing, icon


@callback(
    [
        Output("player", "loop"),
        Output("loop-icon", 'icon')
    ],
    Input("control-repeat", "n_clicks"),
    State("player", "loop"),
    prevent_initial_call=True,
)
def player_loop(n_clicks, loop):
    if not loop == True:
        icon = 'material-symbols:repeat-on'
    else:
        icon = 'material-symbols:repeat'
    return not loop, icon


@callback(
    Output("player", "volume"),
    Input("volume-slider", "value"),
    State("player", "volume"),
    # prevent_initial_call=True,
)
def player_volume(volume_value, current_vol):
    return volume_value / 100


@callback(
    [
        Output("progress-slider", "value"),
        Output("progress-slider", "max"),
        Output("audio-current-time", "children"),
        Output("audio-full-time", "children")
    ],
    Input("player", "currentTime"),
    State("player", "duration"),
    prevent_initial_call=True,
)
def player_volume(currentTime, duration):
    currentTime = int(currentTime) if currentTime != None else 0
    duration = int(duration) if duration != None else 0

    return currentTime, duration, bl_s.get_duration(currentTime), bl_s.get_duration(duration)
