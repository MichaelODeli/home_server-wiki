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
from controllers import cont_homepage
from controllers import service_controller as service

register_page(__name__, path="/", icon="fa-solid:home")


def layout():
    lay = dmc.Container(
        children=[
            dmc.Grid(
                [
                    dmc.GridCol(
                        [cont_homepage.widgetSysteminfo()],
                        span="content",
                        className="adaptive-width",
                        mih='100%'
                    ),
                    dmc.GridCol(
                        [cont_homepage.widgetDiskSize()],
                        span="content",
                        className="adaptive-width",
                        id="t",
                        mih='100%'
                    ),
                    dmc.GridCol(
                        [cont_homepage.widgetTorrents()],
                        span="content",
                        className="adaptive-width",
                        id="widgetTorrents",
                        mih='100%'
                    ),   
                    dmc.GridCol(
                        [cont_homepage.widgetWeather()],
                        span="content",
                        className="adaptive-width", 
                        id="widget-weather",
                        mih='100%'
                    ),                  
                ],
                align="stretch",
                justify="center",
                className="adaptive-block",
            ),
        ],
        pt=20,
        # style={"paddingTop": 20},
        className="dmc-container adaptive-container",
    )

    # print(f'{request.remote_addr} - - [{now}] | homepage {request.base_url}')
    service.logPrinter(request.remote_addr, "homepage", "page opened")
    return lay


@callback(
    [
        Output("home-torrents-active", "children"),
        Output("home-torrents-download", "children"),
        Output("home-torrents-upload", "children"),
    ],
    [Input("t", "children")],
    running=[(Output("loading-overlay-widget-torrent", "visible"), True, False)]
)
def renderTorrentsStatus(_):
    return cont_homepage.getTorrentStatus()
