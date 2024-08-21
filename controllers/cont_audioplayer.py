import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import dcc, html
import pandas as pd


def createTable(df):
    """
    Вывод таблицы на основе Pandas.df
    """
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table


def getButtonGroupWithIcons(lst):
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
                color="secondary",
                style={"display": "flex", "align-items": "start"},
                id=button_id,
                class_name='border white-primary-outline-button'
            )
        )
    return dbc.ButtonGroup(buttons_list, vertical=True)


def audioLeftColumn(source):
    if source != "col" and source != "drawer":
        raise ValueError

    content = dmc.Stack(
        [
            getButtonGroupWithIcons(
                [
                    ["Главная", "home", "audioplayer_mainpage"],
                    ["Поиск музыки", "search", "audioplayer_search"],
                    ["Каталоги музыки", "catalogs", "audioplayer_catalogs"],
                ]
            ),
            dmc.Divider(color="--bs-blue"),
            html.H5("Медиатека"),
            getButtonGroupWithIcons(
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


def getDrawer():
    return dmc.Drawer(
        children=[audioLeftColumn(source="drawer")],
        title=html.H5("Аудиоплеер"),
        id="drawer-albums",
        padding="md",
        zIndex=10000,
        style={'overflow-y': 'auto'}
    )


def floatPlayer():
    return dbc.Card(
        [
            dmc.Grid(
                [
                    dmc.GridCol(
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
                                className="shown-affix",
                            ),
                        ],
                        span="content",
                    ),
                    dmc.GridCol(
                        dmc.Stack(
                            [
                                html.P(
                                    "Название песни",
                                    className="text-default",
                                    style={"margin-bottom": 0, 'font-weight': 'bold'},
                                    id="song-name",
                                ),
                                html.P(
                                    "Исполнитель",
                                    className="text-default",
                                    style={"margin-bottom": 0},
                                    id="song-artist",
                                ),
                            ],
                            gap=0,
                        ),
                        span="content",
                    ),
                    dmc.GridCol(
                        [
                            dmc.Stack(
                                [
                                    dmc.Group(
                                        [
                                            # html.P('Buttons'),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:shuffle",
                                                    width=30,
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-shuffle",
                                                className='hided_element control-button',
                                            ),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:skip-previous",
                                                    width=30,
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-prev",
                                                className='control-button',
                                            ),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:play-pause",
                                                    width=40,
                                                    id='playpause-icon'
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-playpause",
                                                className='control-button',
                                            ),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:skip-next",
                                                    width=30,
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-next",
                                                className='control-button',
                                            ),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:repeat",
                                                    width=30,
                                                    id='loop-icon'
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-repeat",
                                                className='hided_element control-button'
                                            ),
                                        ],
                                        align='center',
                                        style={"justify-content": "center"},
                                        gap='xs'
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
                                                # disabled=True
                                            ),
                                            html.P("59:59", id="audio-full-time", className='hided_element'),
                                        ],
                                        gap="sm",
                                        align='center',
                                        style={"justify-content": "center"},
                                    )
                                ]
                            ),
                        ],
                        span="auto",
                    ),
                    dmc.GridCol(
                        [
                            dbc.Button(
                                DashIconify(
                                    icon="material-symbols:volume-up",
                                    width=30,
                                    id='muted-icon'
                                ),
                                size="20px",
                                color="secondary",
                                outline=True,
                                id="volume-muted",
                                class_name='control-button border border-0'
                            ),
                            dmc.Slider(
                                min=0,
                                max=100,
                                id="volume-slider",
                                value=20,
                                w="120px",
                                color="gray.7",
                                thumbLabel="Громкость",
                                updatemode='drag'
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
