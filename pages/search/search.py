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

register_page(__name__, path="/search", icon="fa-solid:home")


def layout(query=None, **other_unknown_query_strings):
    print(query)
    print(other_unknown_query_strings)
    return dmc.Container(
        children=[
            dmc.Space(h=10),
            dmc.Grid(
                children=[
                    dmc.Col(span="auto"),
                    dmc.Col(
                        children=[
                            html.H4("Поиск")
                        ],
                        span=3,
                        className="block-background",
                    ),
                    dmc.Col(span="auto"),
                ]
            ),
        ],
        pt=20,
        style={"paddingTop": 20},
    )
