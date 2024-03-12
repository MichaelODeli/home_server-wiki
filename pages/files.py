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
from controllers import cont_files as cont_f
from random import randint as r

register_page(__name__, path="/files", icon="fa-solid:home")


def block_files_list():
    return html.Div(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        html.H5("Менеджер файлов", style={"margin": "0"}),
                        span="content",
                    ),
                    dmc.Col(span="auto"),
                    dmc.ButtonGroup(
                        [
                            dmc.Button(
                                "Copy",
                                variant="outline",
                                disabled=True,
                            ),
                            dmc.Button(
                                "Move",
                                variant="outline",
                                disabled=True,
                            ),
                            dmc.Button(
                                "Remove",
                                variant="outline",
                                color="red",
                                disabled=True,
                            ),
                        ],
                        m="5px",
                    ),
                ],
                align="stretch",
                justify="center",
            ),
            dmc.Space(h=15),
            cont_f.generate_html_table(
                ["Маркер", "Название файла", "Размер", "Дата добавления", "Действия"],
                [
                    [
                        DashIconify(icon="material-symbols:folder", width=20),
                        "Перейти в каталог выше",
                        None,
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                ],
            ),
        ],
        className="block-background",
    )


def tree_content(source):
    if source == "col":
        return "Hello! This is on column!"
    elif source == "drawer":
        return "Hello! This is on drawer!"
    else:
        raise ValueError


def get_drawer():
    return dmc.Drawer(
        children=[tree_content(source="drawer")],
        title=html.H5("Дерево папок"),
        id="drawer-tree",
        padding="md",
        zIndex=10000,
    )


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
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dmc.Stack(
                                    [
                                        html.H5("Дерево папок"),
                                        tree_content(source="col")
                                    ],
                                    className="block-background",
                                )
                            ],
                            className="hided_column",
                            width=3
                        ),
                        dbc.Col(
                            [
                                block_files_list(),
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
                get_drawer(),
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
