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

register_page(__name__, path="/players/audioplayer", icon="fa-solid:home")


def layout(l="n", selected_playlist_name='Любимые треки', **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        # now = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        # print(f"{request.remote_addr} - - [{now}] | audioplayer page")
        service.log_printer(request.remote_addr, 'audioplayer', 'page opened')
        df = pd.read_csv(
            "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
        )
        return dmc.Container(
            children=[
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
                                                html.H4(selected_playlist_name, style={'margin-bottom': '0 !important'}),
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
                    style={'width': '100%'},
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
