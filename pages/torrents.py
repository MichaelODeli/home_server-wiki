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
    MATCH,
    ALL,
    callback_context,
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_extensions import Purify
from flask import request
from datetime import datetime
from controllers import service_controller as service
from dash_iconify import DashIconify
import re
import base64

from controllers import cont_torrents as cont_t
from controllers import cont_files as cont_f

register_page(__name__, path="/torrents", icon="fa-solid:home")


def getTorrentButton(
    button_icon, button_title, button_id, disabled=False, color="primary"
):
    return dbc.Button(
        DashIconify(
            icon=button_icon,
            width=25,
        ),
        outline=True,
        color=color,
        id=button_id,
        className="button-center-content p-2",
        title=button_title,
        disabled=disabled,
        size="md",
        n_clicks=0,
    )


def layout(l="n", **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        service.logPrinter(request.remote_addr, "torrents", "page opened")
        # all workers must be here!
        return dmc.Container(
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                dmc.Grid(
                                    [
                                        dmc.GridCol(
                                            html.H5(
                                                "Управление торрентами",
                                                style={"margin": "0"},
                                            ),
                                            span="content",
                                        ),
                                        dmc.GridCol(span="auto"),
                                        dbc.ButtonGroup(
                                            [
                                                getTorrentButton(
                                                    button_icon="material-symbols:sync",
                                                    button_title="Обновить список",
                                                    button_id="torrent-update",
                                                    disabled=False,
                                                ),
                                                getTorrentButton(
                                                    button_icon="material-symbols:add",
                                                    button_title="Добавить торрент",
                                                    button_id="torrent-add",
                                                    # disabled=True,
                                                ),
                                                getTorrentButton(
                                                    button_icon="material-symbols:play-pause",
                                                    button_title="Запустить/остановить торрент",
                                                    button_id="torrent-startstop",
                                                    disabled=True,
                                                ),
                                                getTorrentButton(
                                                    button_icon="material-symbols:info-outline",
                                                    button_title="Информация о торренте",
                                                    button_id="torrent-info",
                                                    disabled=True,
                                                ),
                                                getTorrentButton(
                                                    button_icon="material-symbols:delete",
                                                    button_title="Удалить торрент",
                                                    button_id="torrent-delete",
                                                    color="danger",
                                                    disabled=True,
                                                ),
                                            ],
                                            style={"margin": "5px"},
                                        ),
                                    ],
                                    align="stretch",
                                    justify="center",
                                ),
                                dmc.Space(h=15),
                                html.Div(id="torrents-table-container"),
                            ],
                            className="block-background",
                        ),
                        dmc.Modal(
                            title=html.H5("Добавить торрент"),
                            id="modal-add-torrent",
                            centered=True,
                            size="55%",
                            zIndex=50,
                        ),
                        html.Div(id="torrent-notifications-container"),
                    ],
                ),
            ],
            pt=20,
            # style={"paddingTop": 20},
            className="dmc-container",
        )


@callback(
    Output("modal-add-torrent", "opened", allow_duplicate=True),
    Output("modal-add-torrent", "children"),
    Input("torrent-add", "n_clicks"),
    State("modal-add-torrent", "opened"),
    prevent_initial_call=True,
)
def toggleModal(nc1, opened):
    modal_children = [
        dmc.Stack(
            [
                dcc.Upload(
                    id="upload-torrent",
                    accept=".torrent",
                    children=html.Div(
                        [
                            "Перетащите или ",
                            html.A(
                                "выберите файлы",
                                className="link-opacity-100",
                                href="#",
                            ),
                        ],
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
                    multiple=True,
                ),
                dmc.TextInput(
                    label="Или введите magnet-ссылку", w="100%", id="torrent-magnet"
                ),
                dmc.Button("Скачать по magnet-ссылке", id="torrent-magnet-btn"),
                dmc.Stack(
                    id="torrent-upload-props",
                    children=html.Div(id="torrent-start-download"),
                ),
            ]
        )
    ]
    return not opened, modal_children


@callback(
    Output("modal-add-torrent", "opened"),
    Output("torrent-upload-props", "children"),
    Output("upload-torrent", "disabled"),
    Output("torrent-magnet-btn", "disabled"),
    Output("torrent-magnet", "disabled"),
    Output("torrent-magnet", "error"),
    Input("upload-torrent", "contents"),
    Input("torrent-magnet-btn", "n_clicks"),
    Input("torrent-start-download", "n_clicks"),
    State("upload-torrent", "filename"),
    State("torrent-magnet", "value"),
    prevent_initial_call=True,
)
def parceTorrentFile(
    file_content, n_clicks_magnet, n_clicks_start, file_name, magnet_link=None
):
    dis_upload = True
    dis_magnet_btn = True
    dis_magnet_input = True

    # check link and file
    if n_clicks_magnet != None and magnet_link != "" and magnet_link != None:
        prop_source = "magnet"
        if cont_t.verifyMagnetLink(magnet_link):
            magnet_link = magnet_link
        else:
            return [no_update] * 5 + ["Неверная ссылка"]
    elif file_content != None:
        prop_source = "file"
        for torrent_file in file_content:
            torrent_bytes = base64.b64decode(torrent_file.split(",")[1])
    else:
        return [no_update] * 6

    # add properties of file/url
    properties = [
        html.H6("Информация"),
        dmc.Stack(
            gap="xs",
            children=[
                dmc.Text(
                    f"Для загрузки выбрано {len(file_name)} торрент-файла(ов)."
                    if magnet_link == None or magnet_link == ""
                    else "Для загрузки используется magnet-ссылка."
                ),
            ],
        ),
        dmc.Space(h=7),
        html.H6("Выберите категорию загружаемого файла"),
        dmc.Select(
            placeholder="Выберите",
            id="torrent-category-select",
            value="other",
            data=[
                # value - link with temp-download folder and category, label - category name
                {"value": "films", "label": "Фильмы"},
                {"value": "apps", "label": "Программы"},
                {"value": "serials", "label": "Сериалы"},
                {"value": "other", "label": "Другое"},
            ],
            style={"width": "100%", "margin": "auto"},
        ),
        dbc.Button("Начать загрузку", id="torrent-start-download", disabled=True),
    ]

    # if not download - return properties
    if n_clicks_start == None:
        return (
            no_update,
            properties,
            dis_upload,
            dis_magnet_btn,
            dis_magnet_input,
            False,
        )
    else:
        print("trigger download")
        if prop_source == "magnet":
            print("use magnet")
            # qbt_client.torrents_add(urls=magnet_link)
        elif prop_source == "file":
            print("use file")
            # qbt_client.torrents_add(torrent_files=torrent_bytes)
        else:
            print("unknown")

        return [False] + [no_update] * 5


@callback(
    Output("torrents-table-container", "children"), Input("torrent-update", "n_clicks")
)
def returnTorrentsData(n):
    service.logPrinter(request.remote_addr, "torrents", "toggle update")
    datatable = cont_t.getTorrentsData()
    # datatable = None
    return (
        cont_f.generateHTMLTable(
            header=[
                "",
                "Название файла",
                "Прогресс",
                "Статус",
                "Сиды",
                "Скорость загрузки",
                "Скорость отдачи",
                "Добавлен",
                "Завершен",
            ],
            data=datatable,
            align="center",
            variant="compact",
            striped=True,
            highlightOnHover=True,
        )
        if datatable != None
        else html.H5("Ошибка получения данных", style={"text-align": "center"})
    )


@callback(
    Output("torrents-table-container", "style"),
    Input({"type": "torrent-checkboxes", "id": ALL}, "checked"),
    State({"type": "torrent-checkboxes", "id": ALL}, "id"),
    prevent_initial_call=True,
)
def test(checkboxes_input, checkboxes_ids):
    if [False] * len(checkboxes_input) == checkboxes_input:
        return no_update
    else:
        torrent_ids = []
        for prop_id, checked in zip(checkboxes_ids, checkboxes_input):
            if checked:
                torrent_ids.append(prop_id["id"])

        print(torrent_ids)
        return no_update
