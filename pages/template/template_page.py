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

register_page(__name__, path="/template", icon="fa-solid:home")

def layout(l = 'n', **kwargs):
    # lazy load block
    if l == 'n':
        return dmc.Container()
    else:
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        print(f"{request.remote_addr} - - [{now}] | temp_page")
        # all workers must be here!
        return dmc.Container(
            children=[
                
            ],
            pt=20,
            # style={"paddingTop": 20},
            className='dmc-container',
        )