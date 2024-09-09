from dash import html
import dash_mantine_components as dmc
from controllers.cont_audioplayer import getAudioTypes, getAudioDict
from controllers.cont_media import getDuration
from dash_iconify import DashIconify


def renderMainPage(conn=None):
    return dmc.Stack(
        [
            html.A("Страница исполнителя", href="/players/audio?l=y&artist_id=90", className='a-color'),
            html.A("Страница плейлиста", href="/players/audio?l=y&playlist_id=90", className='a-color'),
            html.A("Страница альбома", href="/players/audio?l=y&album_id=90", className='a-color'),
        ]
    )


def renderSearchPage(conn=None):
    return "Поиск"


def renderPlaylistPage(conn, playlist_id):
    return dmc.Table(
        # hover=True,
        children=[
            dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh(
                            className="min-column-width",
                            px='sm'
                        ),
                        dmc.TableTh(
                            className="min-column-width",
                            px='sm'
                        ),
                        dmc.TableTh(
                            "Название",
                            px='sm'
                        ),
                        dmc.TableTh(
                            "Альбом",
                            className="adaptive-hide",
                            px='sm'
                        ),
                        dmc.TableTh(
                            "Загружено",
                            className="min-column-width center-content adaptive-hide", 
                            px='sm'
                        ),
                        dmc.TableTh(
                            "🕑",
                            className="min-column-width center-content",
                            px='sm'
                        ),
                    ]
                ),
                className="sticky-th",
            ),
            dmc.TableTbody(
                className="audio-content",
                children=[
                    dmc.TableTr(
                        [
                            dmc.TableTd(
                                dmc.ActionIcon(
                                    radius="xl",
                                    children=DashIconify(icon="mdi:play"),
                                ),
                                className="min-column-width p-2",
                            ),
                            dmc.TableTd(
                                dmc.Avatar(radius="sm"),
                                className="min-column-width p-2",
                            ),
                            dmc.TableTd(
                                dmc.Stack(
                                    [
                                        dmc.Text(
                                            audio_data["audio_title"]
                                            if audio_data["audio_title"] is not None
                                            else ".".join(
                                                audio_data["file_name"].split(".")[:-1]
                                            )
                                        ),
                                        html.A(
                                            (
                                                audio_data["artist"]
                                                if audio_data["artist"] is not None
                                                else "Неизвестен"
                                            ),
                                            className="audio-link w-content",
                                            href=f"/file_id={audio_data['file_id']}",
                                        ),
                                    ],
                                    gap=0,
                                ),
                                p='sm'
                            ),
                            dmc.TableTd(
                                html.A(
                                    (
                                        audio_data["album_title"]
                                        if audio_data["album_title"] is not None
                                        else ""
                                    ),
                                    className="audio-link w-content",
                                    href="#",
                                ),
                                className="p-2 adaptive-hide",
                            ),
                            dmc.TableTd(
                                "Недавно",
                                className="min-column-width p-2 adaptive-hide",
                            ),
                            dmc.TableTd(
                                (
                                    getDuration(audio_data["audio_duration"])
                                    if (
                                        audio_data["audio_duration"] is not None
                                    )
                                    else "00:00"
                                ),
                                className="min-column-width p-2",
                            ),
                        ]
                    )
                    for audio_data in getAudioDict(conn, playlist_id)
                ],
            ),
        ],
        className="w-100 no-box-shadow",
        highlightOnHover=True,
    )


def renderArtistPage(artist_id=0):
    return "Какой-то артист"


def renderAlbumPage(album_id=0):
    return "Какой-то альбом"


def renderAudioNavbar(source, conn):
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
        gap=0,
        ms='sm'
    )

    return content


def renderAudioNavbarDrawer(conn):
    return dmc.Drawer(
        children=[renderAudioNavbar(source="drawer", conn=conn)],
        title=dmc.Title("Аудиоплеер", order=4),
        id="drawer-albums",
        padding="md",
        zIndex=10000,
        style={"overflow-y": "auto"},
    )


def renderAudioFooter():
    return dmc.Grid(
        [
            dmc.GridCol(
                [
                    dmc.ActionIcon(
                        DashIconify(
                            icon="iconamoon:menu-burger-horizontal",
                            width=35,
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
