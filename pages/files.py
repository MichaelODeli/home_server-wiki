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
from flask import request
from datetime import datetime
from dash_iconify import DashIconify
from controllers import cont_files as cont_f

register_page(__name__, path="/files", icon="fa-solid:home")


def layout(l="n", **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        print(f"{request.remote_addr} - - [{now}] | files page")
        return dmc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dmc.Stack(
                                    [
                                        html.H5("Дерево папок"),
                                        cont_f.tree_content(source="col")
                                    ],
                                    className="block-background",
                                )
                            ],
                            className="hided_column",
                            width=3,
                        ),
                        dbc.Col(
                            [
                                cont_f.block_files_list(),
                            ]
                        ),
                    ]
                ),
                dmc.Affix(
                    dmc.ActionIcon(
                        DashIconify(
                            icon="iconamoon:menu-burger-horizontal",
                            width=35,
                            color="var(--bs-primary)",
                        ),
                        size="xl",
                        radius="xl",
                        variant="default",
                        id="open-drawer",
                    ),
                    position={"bottom": 20, "left": 20},
                    className="shown_affix",
                ),
                cont_f.get_drawer(),
            ],
            pt=20,
            className="dmc-container adaptive-container",
        )


@callback(
    Output("drawer-tree", "opened"),
    Input("open-drawer", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_with_tree(n_clicks):
    return True
