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
from flask import request

register_page(__name__, path="/", icon="fa-solid:home")

def layout():
    lay = dmc.Container(
        children=[],
        pt=20,
        style={"paddingTop": 20},
    )
    print('client ip', request.remote_addr)
    print('server link', request.base_url)
    return lay