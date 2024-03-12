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
from flask import request
from datetime import datetime
from dash_iconify import DashIconify
from controllers import cont_homepage as cont_h

register_page(__name__, path="/files", icon="fa-solid:home")


def layout(l="n", **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        print(f"{request.remote_addr} - - [{now}] | files page")
        # all workers must be here!
        return dmc.Container(
            children=[
                html.Div(
                    [
                        dmc.Grid(
                            [
                                dmc.Col("Менеджер файлов", span="content"),
                                dmc.Col(span="auto"),
                                dmc.ButtonGroup(
                                    [
                                        dmc.Button("Скопировать", variant="outline", disabled=True, ),
                                        dmc.Button("Переместить", variant="outline", disabled=True),
                                        dmc.Button("Удалить", variant="outline", color='red', disabled=True),
                                    ],
                                    m='5px' 
                                ),
                            ],
                            align="stretch",
                            justify="center",
                        )
                    ],
                    className="block-background",
                )
            ],
            pt=20,
            className="dmc-container adaptive-container",
        )
