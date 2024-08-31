import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import dcc, html
import pandas as pd
from psycopg2.extensions import AsIs


def getAudioTypes(conn, type_id=None):
    with conn.cursor() as cursor:
        cursor.execute(
            """select * from (select distinct(type_id) from filestorage_mediafiles_summary fms where html_audio_ready)
                left join (select id as type_id, type_name from filestorage_types) ft using(type_id) %(addition)s;""",
            {"addition": AsIs(f"WHERE type_id = {type_id}" if type_id else "")},
        )

        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data


def createTable(df):
    """
    Вывод таблицы на основе Pandas.df
    """
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table


def getAudioIcon(icon_prefix):
    audioplayer_icons = {
        "playlist": "material-symbols:playlist-play",
        "genre": "material-symbols:genres",
        "artist": "material-symbols:artist",
        "home": "material-symbols:home",
        "search": "material-symbols:search",
        "catalogs": "material-symbols:folder-open",
    }

    return DashIconify(
        icon=audioplayer_icons[icon_prefix],
        width=25,
        style={"margin-right": "5px"},
    )


def getButtonGroupWithIcons(lst):
    """
    Вывод вертикальной группы с кнопками и иконками.
    Формат вложенного списка: [[button_text, button_icon_name, button_id, add_icon, disbled_button], ...]
    """
    buttons_list = []
    for element in lst:
        button_text = element[0]
        button_icon_name = element[1]
        button_id = element[2]
        add_icon = element[3]
        disbled_button = element[4]
        if add_icon:
            icon = getAudioIcon(button_icon_name)
        else:
            icon = None

        buttons_list.append(
            dbc.Button(
                children=[icon, button_text],
                outline=True,
                color="secondary",
                style={"display": "flex", "align-items": "start"},
                id=button_id,
                class_name="border white-primary-outline-button",
                disabled=disbled_button,
            )
        )
    return dbc.ButtonGroup(buttons_list, vertical=True)


def audioLeftColumn(source, conn):
    if source != "col" and source != "drawer":
        raise ValueError

    content = dmc.Stack(
        [
            getButtonGroupWithIcons(
                [
                    [
                        "Главная",
                        "home",
                        {"type": f"audio-playlist-btn-home", "id": 1},
                        True,
                        False,
                    ],
                    [
                        "Поиск музыки",
                        "search",
                        {"type": f"audio-playlist-btn-search", "id": 1},
                        True,
                        False,
                    ],
                ]
            ),
            html.H5("Медиатека"),
            dbc.ButtonGroup(
                children=[
                    dbc.Button(
                        children=[
                            DashIconify(
                                icon="material-symbols:playlist-play",
                                width=25,
                                style={"margin-right": "5px"},
                            ),
                            audio_type["type_name"],
                        ],
                        outline=True,
                        color="secondary",
                        style={"display": "flex", "align-items": "start"},
                        id={
                            "type": f"audio-playlist-btn-{source}",
                            "id": audio_type["type_id"],
                        },
                        class_name="border white-primary-outline-button",
                    )
                    for audio_type in getAudioTypes(conn)
                ],
                vertical=True,
            ),
        ]
    )

    return content


def getDrawer(conn):
    return dmc.Drawer(
        children=[audioLeftColumn(source="drawer", conn=conn)],
        title=html.H5("Аудиоплеер"),
        id="drawer-albums",
        padding="md",
        zIndex=10000,
        style={"overflow-y": "auto"},
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
                                    # color="var(--bs-primary)",
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
                                    style={"margin-bottom": 0, "font-weight": "bold"},
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
                                                    width=25,
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-shuffle",
                                                className="hided_element control-button",
                                            ),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:skip-previous",
                                                    width=25,
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-prev",
                                                className="control-button",
                                            ),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:play-pause",
                                                    width=25,
                                                    id="playpause-icon",
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-playpause",
                                                className="control-button",
                                            ),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:skip-next",
                                                    width=25,
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-next",
                                                className="control-button",
                                            ),
                                            dbc.Button(
                                                DashIconify(
                                                    icon="material-symbols:repeat",
                                                    width=25,
                                                    id="loop-icon",
                                                ),
                                                size="20px",
                                                color="secondary",
                                                outline=True,
                                                id="control-repeat",
                                                className="hided_element control-button",
                                            ),
                                        ],
                                        align="center",
                                        style={"justify-content": "center"},
                                        gap="xs",
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
                                            html.P(
                                                "59:59",
                                                id="audio-full-time",
                                                className="hided_element",
                                            ),
                                        ],
                                        gap="sm",
                                        align="center",
                                        style={"justify-content": "center"},
                                    ),
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
                                    id="muted-icon",
                                ),
                                size="20px",
                                color="secondary",
                                outline=True,
                                id="volume-muted",
                                class_name="control-button border border-0 no-box-shadow",
                            ),
                            dmc.Slider(
                                min=0,
                                max=100,
                                id="volume-slider",
                                value=20,
                                w="120px",
                                color="gray.7",
                                thumbLabel="Громкость",
                                updatemode="drag",
                            ),
                        ],
                        span="content",
                        style={"align-items": "center", "display": "flex"},
                        className="hided_element",
                    ),
                ],
                align="center",
                justify="center",
            )
        ],
        style={"min-height": "70px", "background-color": "var(--bs-body-bg)"},
        className="block-background-float",
    )
