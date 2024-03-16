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
from controllers import service_controller as service

register_page(__name__, path="/torrents", icon="fa-solid:home")


def layout(l="n", **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        service.log_printer(request.remote_addr, "torrents", "page opened")
        # all workers must be here!
        return dmc.Container(
            children=[
                dmc.Stack(
                    [
                        html.P("Добавка торрентов на закачку по категориям"),
                        html.P("Мини-таблица с текущими торрентами"),
                    ]
                )
            ],
            pt=20,
            # style={"paddingTop": 20},
            className="dmc-container",
        )
