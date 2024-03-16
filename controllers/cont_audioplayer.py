import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import dcc, html
import pandas as pd


def create_table(df):
    """
    Вывод таблицы на основе Pandas.df
    """
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table


def get_buttongroup_with_icons(lst):
    """
    Вывод вертикальной группы с кнопками и иконками.
    Формат вложенного списка: [[button_text, button_icon_name, button_id], ...]
    """
    buttons_list = []
    for element in lst:
        button_text = element[0]
        button_icon_name = element[1]
        button_id = element[2]
        if button_icon_name == "playlist":
            icon_name = "material-symbols:playlist-play"
        elif button_icon_name == "genre":
            icon_name = "material-symbols:genres"
        elif button_icon_name == "artist":
            icon_name = "material-symbols:artist"
        elif button_icon_name == "home":
            icon_name = "material-symbols:home"
        elif button_icon_name == "search":
            icon_name = "material-symbols:search"
        elif button_icon_name == "catalogs":
            icon_name = "material-symbols:folder-open"
        else:
            icon_name = None

        icon = (
            DashIconify(icon=icon_name, width=25, style={"margin-right": "5px"})
            if icon_name != None
            else None
        )

        buttons_list.append(
            dbc.Button(
                children=[icon, button_text],
                outline=True,
                color="primary",
                style={"display": "flex", "align-items": "start"},
                id=button_id,
            )
        )
    return dbc.ButtonGroup(buttons_list, vertical=True)


def audio_leftcollumn(source):
    if source != "col" and source != "drawer":
        raise ValueError

    content = dmc.Stack(
        [
            get_buttongroup_with_icons(
                [
                    ["Главная", "home", "audioplayer_mainpage"],
                    ["Поиск музыки", "search", "audioplayer_search"],
                    ["Каталоги музыки", "catalogs", "audioplayer_catalogs"],
                ]
            ),
            dmc.Divider(color="--bs-blue"),
            html.H5("Медиатека"),
            get_buttongroup_with_icons(
                [
                    ["Любимые треки", "playlist", "id_1"],
                    ["My favourite rock", "playlist", "id_2"],
                    ["AC/DC", "artist", "id_3"],
                    ["Rammstein", "artist", "id_4"],
                    ["Рок", "genre", "id_5"],
                    ["Хаус", "genre", "id_6"],
                ]
            ),
        ]
    )

    return content


def get_drawer():
    return dmc.Drawer(
        children=[audio_leftcollumn(source="drawer")],
        title=html.H5("Аудиоплеер"),
        id="drawer-albums",
        padding="md",
        zIndex=10000,
        style={'overflow-y': 'auto'}
    )


def float_player():
    return html.Div(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.ActionIcon(
                                DashIconify(
                                    icon="iconamoon:menu-burger-horizontal",
                                    width=35,
                                    color="var(--bs-primary)",
                                ),
                                size="40px",
                                radius="md",
                                variant="default",
                                id="open-drawer-albums",
                                className="shown_affix",
                            ),
                        ],
                        span="content",
                    ),
                    dmc.Col(
                        dmc.Stack(
                            [
                                html.P(
                                    "Название песни",
                                    className="text-primary",
                                    style={"margin-bottom": 0},
                                    id="song-name",
                                ),
                                html.P(
                                    "Исполнитель",
                                    className="text-secondary",
                                    style={"margin-bottom": 0},
                                    id="song-artist",
                                ),
                            ],
                            spacing=0,
                        ),
                        span="content",
                    ),
                    dmc.Col(
                        [
                            dmc.Stack(
                                [
                                    dmc.Group(
                                        [
                                            # html.P('Buttons'),
                                            dmc.ActionIcon(
                                                DashIconify(
                                                    icon="material-symbols:shuffle",
                                                    width=40,
                                                    color="var(--bs-primary)",
                                                ),
                                                size="35px",
                                                variant="default",
                                                id="control-shuffle",
                                                className='hided_element'
                                            ),
                                            dmc.ActionIcon(
                                                DashIconify(
                                                    icon="material-symbols:skip-previous",
                                                    width=40,
                                                    color="var(--bs-primary)",
                                                ),
                                                size="35px",
                                                variant="default",
                                                id="control-prev",
                                            ),
                                            dmc.ActionIcon(
                                                DashIconify(
                                                    icon="material-symbols:play-pause",
                                                    width=45,
                                                    color="var(--bs-primary)",
                                                ),
                                                size="40px",
                                                variant="default",
                                                id="control-playpause",
                                            ),
                                            dmc.ActionIcon(
                                                DashIconify(
                                                    icon="material-symbols:skip-next",
                                                    width=40,
                                                    color="var(--bs-primary)",
                                                ),
                                                size="35px",
                                                variant="default",
                                                id="control-next",
                                            ),
                                            dmc.ActionIcon(
                                                DashIconify(
                                                    icon="material-symbols:repeat",
                                                    width=40,
                                                    color="var(--bs-primary)",
                                                ),
                                                size="35px",
                                                variant="default",
                                                id="control-repeat",
                                                className='hided_element'
                                            ),
                                        ],
                                        align='center',
                                        style={"justify-content": "center"},
                                        spacing='xs'
                                    ),
                                    dmc.Group(
                                        [
                                            html.P("00:00", id="audio-current-time"),
                                            dmc.Slider(
                                                min=0,
                                                max=100,
                                                id="progress-slider",
                                                value=0,
                                                w="70%",
                                                color="gray.7",
                                                showLabelOnHover=False,
                                            ),
                                            html.P("99:99", id="audio-full-time", className='hided_element'),
                                        ],
                                        spacing="sm",
                                        align='center',
                                        style={"justify-content": "center"},
                                    )
                                ]
                            ),
                        ],
                        span="auto",
                    ),
                    dmc.Col(
                        [
                            dmc.Slider(
                                min=0,
                                max=100,
                                id="volume-slider",
                                value=50,
                                w="120px",
                                color="gray.7",
                                thumbLabel="Громкость",
                            ),
                        ],
                        span="content",
                        style={"align-items": "center", "display": "flex"},
                        className="hided_element",
                    ),
                ],
                align="center",
                justify='center'
            )
        ],
        style={
            "min-height": "70px",
        },
        className="block-background-float",
    )
