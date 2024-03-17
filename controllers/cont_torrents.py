import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import dcc, html


def add_torrent_modal():
    return dmc.Modal(
        title=html.H5("Добавить торрент"),
        id="modal-add-torrent",
        centered=True,
        size="55%",
        zIndex=10000,
        children=[
            dmc.Stack(
                [
                    dcc.Upload(
                        id="upload-torrent",
                        children=html.Div(
                            ["Перетащите или ", html.A("выберите файлы")]
                        ),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            # "margin": "10px",
                        },
                        # Allow multiple files to be uploaded
                        # multiple=True,
                    ),
                    dmc.Select(
                        label=html.P("Выберите категорию загружаемого файла", className='H5'),
                        placeholder="Выберите",
                        id="torrent-category-select",
                        value="other",
                        data=[
                            {"value": "films", "label": "Фильмы"},
                            {"value": "apps", "label": "Программы"},
                            {"value": "serials", "label": "Сериалы"},
                            {"value": "other", "label": "Другое"},
                        ],
                        style={"width": "90%", "margin": "auto"},
                    ),
                    dbc.Button("Начать загрузку", id='torrent-start-download', n_clicks=0)
                ]
            )
        ],
    )


def block_torrents():
    return html.Div(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        html.H5("Управление торрентами", style={"margin": "0"}),
                        span="content",
                    ),
                    dmc.Col(span="auto"),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                DashIconify(icon="material-symbols:add", width=25),
                                outline=True,
                                color="primary",
                                id="torrent-add",
                                className="button-center-content",
                                title="Добавить торрент",
                                # disabled=True,
                                size="md",
                                n_clicks=0
                            ),
                            dbc.Button(
                                DashIconify(
                                    icon="material-symbols:play-pause", width=25
                                ),
                                outline=True,
                                color="primary",
                                id="torrent-startstop",
                                className="button-center-content",
                                title="Запустить/остановить торрент",
                                disabled=True,
                                size="md",
                            ),
                            dbc.Button(
                                DashIconify(
                                    icon="material-symbols:info-outline", width=25
                                ),
                                outline=True,
                                color="primary",
                                id="torrent-info",
                                className="button-center-content",
                                title="Информация о торренте",
                                disabled=True,
                                size="md",
                            ),
                            dbc.Button(
                                DashIconify(icon="material-symbols:delete", width=25),
                                outline=True,
                                color="danger",
                                id="torrent-delete",
                                className="button-center-content",
                                title="ОПИСАНИЕ",
                                disabled=True,
                                size="md",
                            ),
                        ],
                        style={"margin": "5px"},
                    ),
                ],
                align="stretch",
                justify="center",
            ),
            dmc.Space(h=150),
        ],
        className="block-background",
    )
