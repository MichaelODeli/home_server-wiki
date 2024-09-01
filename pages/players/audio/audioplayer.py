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
    ALL,
    ctx,
    callback_context,
)
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from flask import request
from controllers import (
    cont_audioplayer as cont_a,
    service_controller as service,
    cont_search as cont_s,
    cont_media as cont_m,
    db_connection,
    file_manager,
)
from views import v_audioplayer
import dash_player

register_page(__name__, path="/players/audio", icon="fa-solid:home")


def layout(l="n", playlist_id=0, artist_id=0, album_id=0, **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        service.logPrinter(request.remote_addr, "audioplayer", "page opened")

        conn = db_connection.getConn()

        if playlist_id == 0 and artist_id == 0 and album_id == 0:
            page_name = "Главная"
            page_content = v_audioplayer.renderMainPage()
        else:
            if playlist_id != 0 and artist_id == 0 and album_id == 0:
                page_name = "Какой-то плейлист"
                page_content = v_audioplayer.renderPlaylistPage()
            elif artist_id != 0 and playlist_id == 0 and album_id == 0:
                page_name = "Какой-то исполнитель"
                page_content = v_audioplayer.renderArtistPage()
            elif album_id != 0 and playlist_id == 0 and artist_id == 0:
                page_name = "Какой-то альбом"
                page_content = v_audioplayer.renderAlbumPage()
            else:
                page_name = ""
                page_content = html.Center(html.H6("Ошибка идентификатора."))

        return dmc.AppShell(
            children=[
                dmc.AppShellNavbar(
                    cont_a.audioLeftColumn(source="col", conn=conn),
                    className="border-end-0",
                ),
                dmc.AppShellMain(
                    [
                        dash_player.DashPlayer(
                            id="audio-player",
                            url="https://www.youtube.com/watch?v=4xnsmyI5KMQ&t=1s",
                            width="0",
                            height="0",
                            style={"display": "none"},
                            intervalCurrentTime=500,
                            volume=20,
                        ),
                        dmc.Space(),
                        dmc.Stack(
                            [
                                html.H3(
                                    page_name,
                                    style={"margin-bottom": "0 !important"},
                                    id="audioplayer-playlist-name",
                                ),
                                dmc.Space(),
                                dmc.Group(id="audio-playlist-description"),
                                dmc.ScrollArea(
                                    children=page_content,
                                    # className="w-100 overflow-auto",
                                    id="audioplayer-children",
                                    pb='sm',
                                    h='70dvh',
                                    offsetScrollbars=True
                                ),
                            ],
                            gap="xs",
                        ),
                        cont_a.getDrawer(conn),
                    ],
                    className="ps-3 pt-1 border-start overflow-hidden no-border-mobile",
                    mah='calc(100dvh - var(--app-shell-header-height) - 10px) !important',
                    mih='calc(100dvh - var(--app-shell-header-height) - 10px) !important',
                ),
                dmc.AppShellFooter(cont_a.floatPlayer()),
            ],
            navbar={
                "width": 300,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
            footer={"height": "auto"},
            pt=20,
            className="adaptive-container",
            id="dummy-3",
            # mah="90dvh",
        )


@callback(
    Output("drawer-albums", "opened", allow_duplicate=True),
    Input("open-drawer-albums", "n_clicks"),
    prevent_initial_call=True,
)
def drawerWithAlbums(n_clicks):
    return True


@callback(
    [Output("audio-player", "playing"), Output("playpause-icon", "icon")],
    Input("control-playpause", "n_clicks"),
    State("audio-player", "playing"),
    prevent_initial_call=True,
)
def playerPlayPause(n_clicks, playing):
    if not playing == True:
        icon = "material-symbols:pause"
    else:
        icon = "material-symbols:play-arrow"
    return not playing, icon


@callback(
    [Output("audio-player", "loop"), Output("loop-icon", "icon")],
    Input("control-repeat", "n_clicks"),
    State("audio-player", "loop"),
    prevent_initial_call=True,
)
def playerLoop(n_clicks, loop):
    if not loop == True:
        icon = "material-symbols:repeat-on"
    else:
        icon = "material-symbols:repeat"
    return not loop, icon


@callback(
    [Output("audio-player", "muted"), Output("muted-icon", "icon")],
    Input("volume-muted", "n_clicks"),
    State("audio-player", "muted"),
    prevent_initial_call=True,
)
def playerDisableSound(n_clicks, muted):
    if not muted == True:
        icon = "material-symbols:volume-off"
    else:
        icon = "material-symbols:volume-up"
    return not muted, icon


@callback(
    Output("audio-player", "volume"),
    Input("volume-slider", "value"),
    State("audio-player", "volume"),
    # prevent_initial_call=True,
)
def playerVolumeSlider(volume_value, current_vol):
    return volume_value / 100


@callback(
    [
        Output("progress-slider", "value"),
        Output("progress-slider", "max"),
        Output("audio-current-time", "children"),
        Output("audio-full-time", "children"),
    ],
    Input("audio-player", "currentTime"),
    State("audio-player", "duration"),
    prevent_initial_call=True,
)
def playerVolume(currentTime, duration):
    currentTime = int(currentTime) if currentTime != None else 0
    duration = int(duration) if duration != None else 0

    return (
        currentTime,
        duration,
        cont_m.getDuration(currentTime),
        cont_m.getDuration(duration),
    )


@callback(
    Output({"type": "audio-playlist-btn-col", "id": ALL}, "n_clicks"),
    Output({"type": "audio-playlist-btn-drawer", "id": ALL}, "n_clicks"),
    Output("audioplayer-playlist-name", "children"),
    Output("drawer-albums", "opened"),
    Output("audio-playlist-description", "children"),
    Output("audioplayer-children", "children"),
    Input({"type": "audio-playlist-btn-col", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-drawer", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-home", "id": ALL}, "n_clicks"),
    Input({"type": "audio-playlist-btn-search", "id": ALL}, "n_clicks"),
    State({"type": "audio-playlist-btn-col", "id": ALL}, "id"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def selectPlaylistFromLeftsideRow(
    n_clicks_col, n_clicks_drawer, n_clicks_home, n_clicks_search, button_ids, pathname
):

    types_ids = [i["id"] for i in button_ids]

    if (
        n_clicks_col == [None] * len(n_clicks_col)
        and n_clicks_drawer == [None] * len(n_clicks_drawer)
        and n_clicks_home == [None] * len(n_clicks_home)
        and n_clicks_search == [None] * len(n_clicks_search)
    ):
        raise PreventUpdate

    description = None
    if ctx.triggered_id["type"] == "audio-playlist-btn-home":
        page_name = "Главная"
        player_children = [v_audioplayer.renderMainPage()]
    elif ctx.triggered_id["type"] == "audio-playlist-btn-search":
        page_name = "Поиск"
        player_children = [v_audioplayer.renderSearchPage()]
    else:
        description = [
            dmc.Badge("1250 треков", variant="light"),
            dmc.Badge("500 минут", variant="light"),
        ]

        if ctx.triggered_id["type"] == "audio-playlist-btn-col":
            selected_type = types_ids[n_clicks_col.index(1)]
        elif ctx.triggered_id["type"] == "audio-playlist-btn-drawer":
            selected_type = types_ids[n_clicks_drawer.index(1)]
        else:
            raise PreventUpdate

        conn = db_connection.getConn()
        page_name = cont_a.getAudioTypes(conn, type_id=selected_type)[0]["type_name"]

        player_children = v_audioplayer.renderPlaylistPage()

    return (
        [None] * len(n_clicks_col),
        [None] * len(n_clicks_drawer),
        page_name,
        False,
        description,
        player_children,
    )
