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

register_page(__name__, path="/settings", icon="fa-solid:home")

def layout(): 
    return dmc.Container(
        children=[
            dmc.Space(h=10),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Основные настройки", value="main"),
                            dmc.Tab("Настройки сервера", value="server"),
                            dmc.Tab("Обработчик файлов", value="files"),
                        ],
                        grow=True
                    ),
                    dmc.TabsPanel(children=["Tab content"], value="main"),
                    dmc.TabsPanel(children=["Tab content"], value="server"),
                    dmc.TabsPanel(children=["Tab content"], value="files"),
                ],
                variant="outline",
                orientation="vertical",
                className='block-background'
            )
        ],
        pt=20,
        style={"paddingTop": 20},
    )