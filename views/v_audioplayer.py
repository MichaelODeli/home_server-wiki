from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def renderMainPage():
    return dmc.Stack(
        [
            html.A('Страница исполнителя', href='/players/audio?l=y&artist_id=90'),
            html.A('Страница плейлиста', href='/players/audio?l=y&playlist_id=90'),
            html.A('Страница альбома', href='/players/audio?l=y&album_id=90'),

        ]
    )


def renderSearchPage():
    return "Поиск"


def renderPlaylistPage(playlist_id=0):
    return dmc.Table(
        # hover=True,
        children=[
            dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh(
                            className="min-column-width px-2",
                        ),
                        dmc.TableTh(
                            className="min-column-width px-2",
                        ),
                        dmc.TableTh(
                            "Название",
                            className="px-2",
                        ),
                        dmc.TableTh(
                            "Альбом",
                            className="px-2 adaptive-hide",
                        ),
                        dmc.TableTh(
                            "Загружено",
                            className="min-column-width px-2 adaptive-hide",
                        ),
                        dmc.TableTh(
                            "🕑",
                            className="min-column-width px-2 center-content",
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
                                        dmc.Text("Название трека"),
                                        html.A(
                                            "Исполнитель",
                                            className="audio-link w-content",
                                            href="#",
                                        ),
                                    ],
                                    gap=0,
                                ),
                                className="p-2",
                            ),
                            dmc.TableTd(
                                html.A(
                                    "Альбом",
                                    className="audio-link w-content",
                                    href="#",
                                ),
                                className="p-2 adaptive-hide",
                            ),
                            dmc.TableTd(
                                "Вчера",
                                className="min-column-width p-2 adaptive-hide",
                            ),
                            dmc.TableTd(
                                "3:15",
                                className="min-column-width p-2",
                            ),
                        ]
                    )
                ]
                * 20,
            ),
        ],
        className="w-100 no-box-shadow",
        highlightOnHover=True,
    )


def renderArtistPage(artist_id=0):
    return "Какой-то артист"


def renderAlbumPage(album_id=0):
    return "Какой-то альбом"
