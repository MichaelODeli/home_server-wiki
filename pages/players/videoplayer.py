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
import sqlite3
import dash_mantine_components as dmc
import dash_player as dp
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

register_page(__name__, path="/players/videoplayer", icon="fa-solid:home")

link = ''

def get_video_card(video_title, video_length, video_link):
    return html.A([dmc.Card(
            children=[
                dmc.CardSection(
                    dmc.Image(
                        src="/assets/image-not-found.jpg",
                        height=120,
                    )
                ),
                dmc.Group(
                    [
                        dmc.Text(str(video_title), weight=500),
                        dbc.Badge(str(video_length), text_color="primary", className="border me-1", color='white'),
                    ],
                    position="apart",
                    mt="md",
                    mb="xs",
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"width": 'auto'}, # prev: 350px
        )], href=video_link)

def layout(v=None, v_type='youtube', **other_unknown_query_strings):
    global link
    if v!=None:
        conn = sqlite3.connect('bases/nstorage.sqlite3')
        c = conn.cursor()
        c.execute(f"SELECT * FROM {v_type} WHERE {v_type}_filehash = '{v}'")
        one_result = c.fetchone()
        channel = one_result[1]
        filename = one_result[2]
        name = '.'.join(filename.split('.')[:-1])
        link = f'http://192.168.3.33/storage/{v_type}/{channel}/{filename}'
        c.close()
        conn.close()
    else:
        channel = 'Sample'
        name = 'Big buck bunny'
        link = 'https://www.w3schools.com/html/mov_bbb.mp4'

    return dmc.Container(
        children=[
            dmc.Space(h=10),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dp.DashPlayer(
                                id="player",
                                url=link,
                                controls=True,
                                width="1200px",
                                className="video_container",
                                volume=0.4
                            ),
                            dmc.Space(h=5),
                            html.H4(name, style={"width": "100%"}, id='player_videoname'),
                            dmc.Space(h=10),
                            dmc.Grid(
                                children=[
                                    dmc.Col(
                                        dmc.Center(
                                            dmc.Button(
                                                html.A(
                                                    channel,
                                                    href=f"/search?from_video_view=True&query={channel}",
                                                    style={"textDecoration": "none"},
                                                    id='player_channelLink'
                                                ),
                                                compact=True,
                                                variant="subtle",
                                                color="black",
                                            )
                                        ),
                                        span="content",
                                    ),
                                    dmc.Col(span="auto"),
                                    dmc.Col(
                                        dmc.Group(
                                            children=[
                                                dmc.ActionIcon(
                                                    DashIconify(
                                                        icon="material-symbols:download-for-offline-outline-rounded",
                                                        width=20,
                                                    ),
                                                    # compact=True,
                                                    variant="subtle",
                                                    color="black",
                                                    id='player_download',
                                                    disabled=True,
                                                ),
                                                dmc.ActionIcon(
                                                    DashIconify(
                                                        icon="material-symbols:playlist-add-rounded",
                                                        width=20,
                                                    ),
                                                    # compact=True,
                                                    variant="subtle",
                                                    color="black",
                                                    id='player_addToPlaylist',
                                                    disabled=True,
                                                ),
                                                dmc.ActionIcon(
                                                    DashIconify(
                                                        icon="material-symbols:flag-outline-rounded",
                                                        width=20,
                                                    ),
                                                    # compact=True,
                                                    variant="subtle",
                                                    color="black",
                                                    id='player_report',
                                                    disabled=True,
                                                ),
                                            ],
                                            spacing='xs'
                                        ),
                                        span="content",
                                    ),
                                ],
                                align="center",
                                style={"width": "100%"},
                            ),
                        ],
                        className="block-background mrrow video-column",
                        width="auto",
                    ),
                    dbc.Col(children=[
                        html.H5('Смотрите также:'),
                        dbc.ButtonGroup(
                            [dbc.Button("Рекомендации", disabled=True, outline=True), dbc.Button(f'Канал: {channel}'), dbc.Button("Похожие", disabled=True, outline=True)],
                        style={'width': '100%'}),
                        dmc.Space(h=7),
                        get_video_card('Sample video 1', '00:50', 'https://example.com'),
                        dmc.Space(h=7),
                        get_video_card('Sample video 2', '01:50', 'https://example.com'),
                        dmc.Space(h=7),
                        get_video_card('Sample video 3', '02:50', 'https://example.com'),
                        dmc.Space(h=7),
                        get_video_card('Sample video 4', '03:50', 'https://example.com'),
                        dmc.Space(h=7),
                        get_video_card('Sample video 5', '1:04:50', 'https://example.com'),
                    ], className="block-background mrrow overflow-column"),
                ],
                className="gx-3",
            ),
        ],
        pt=20,
        style={"paddingTop": 20},
        size="98%",
    )