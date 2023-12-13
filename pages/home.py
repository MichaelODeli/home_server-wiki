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
from datetime import datetime 

register_page(__name__, path="/", icon="fa-solid:home")

def layout():
    lay = dmc.Container(
        children=[],
        pt=20,
        style={"paddingTop": 20},
    )
    now = datetime.now().strftime("%H:%M:%S")
    print(f'{now} | client {request.remote_addr} | homepage {request.base_url}')
    return lay