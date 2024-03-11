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
from blocks import bl_homepage as bl_h

import locale
locale.setlocale(locale.LC_ALL, 'ru_RU')

register_page(__name__, path="/", icon="fa-solid:home")

def layout():
    lay = dmc.Container(
        children=[
            dmc.Grid([
                dmc.Col(span='auto'),
                dmc.Col([bl_h.block_disk_size()], span='content', className='mobile-block'),
                dmc.Col([bl_h.block_weather()], span='content', className='mobile-block'),
                dmc.Col(span='auto')
            ],
            className='grid-home')
        ],
        pt=20,
        # style={"paddingTop": 20},
        className='dmc-container home-container'
    )
    now = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    # print(f'{request.remote_addr} - - [{now}] | homepage {request.base_url}')
    print(f"{request.remote_addr} - - [{now}] | homepage")
    return lay
