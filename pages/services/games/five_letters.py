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

register_page(__name__, path="/services/games/five_letters", icon="fa-solid:home")

layout = dmc.Container(
    children=[],
    pt=20,
    style={"paddingTop": 20},
)