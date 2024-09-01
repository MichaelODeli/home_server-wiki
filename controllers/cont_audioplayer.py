import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import dcc, html
import pandas as pd
from psycopg2.extensions import AsIs
from random import randint


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


def audioLeftColumn(source, conn):
    if source != "col" and source != "drawer":
        raise ValueError

    content = dmc.Stack(
        [
            dmc.NavLink(
                leftSection=DashIconify(
                    icon="material-symbols:home",
                    width=25,
                    style={"margin-right": "5px"},
                ),
                label="Главная",
                id={
                    "type": "audio-playlist-btn-home",
                    "id": 1 if source == "col" else 2,
                },
            ),
            dmc.NavLink(
                leftSection=DashIconify(
                    icon="material-symbols:search",
                    width=25,
                    style={"margin-right": "5px"},
                ),
                label="Поиск музыки",
                id={
                    "type": "audio-playlist-btn-search",
                    "id": 1 if source == "col" else 2,
                },
            ),
            dmc.NavLink(
                leftSection=DashIconify(
                    icon="mdi:music",
                    width=25,
                    style={"margin-right": "5px"},
                ),
                label="Медиатека",
                opened=True,
                children=[
                    dmc.NavLink(
                        leftSection=DashIconify(
                            icon="material-symbols:playlist-play",
                            width=25,
                            style={"margin-right": "5px"},
                        ),
                        label=audio_type["type_name"],
                        id={
                            "type": f"audio-playlist-btn-{source}",
                            "id": audio_type["type_id"],
                        },
                    )
                    for audio_type in getAudioTypes(conn)
                ],
            ),
        ],
        className="px-1",
        gap=0,
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
    return dmc.Grid(
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
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:shuffle",
                                            width=25,
                                            color="dark",
                                        ),
                                        id="control-shuffle",
                                        className="adaptive-hide",
                                        variant="subtle",
                                        size="lg",
                                        color="default",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:skip-previous",
                                            width=25,
                                            color="dark",
                                        ),
                                        id="control-prev",
                                        variant="subtle",
                                        size="lg",
                                        color="default",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:play-pause",
                                            width=30,
                                            id="playpause-icon",
                                        ),
                                        id="control-playpause",
                                        variant="filled",
                                        size="xl",
                                        radius="xl",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:skip-next",
                                            width=25,
                                            color="dark",
                                        ),
                                        id="control-next",
                                        variant="subtle",
                                        size="lg",
                                        color="default",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="material-symbols:repeat",
                                            width=25,
                                            color="dark",
                                            id="loop-icon",
                                        ),
                                        id="control-repeat",
                                        variant="subtle",
                                        size="lg",
                                        color="default",
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
                    dmc.ActionIcon(
                        DashIconify(
                            icon="material-symbols:volume-up",
                            width=30,
                            color="dark",
                            id="muted-icon",
                        ),
                        id="volume-muted",
                        variant="subtle",
                        size="xl",
                        color="default",
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
        className="block-background-float",
    )
