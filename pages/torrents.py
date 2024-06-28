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
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_extensions import Purify
from flask import request
from datetime import datetime
from controllers import service_controller as service
from dash_iconify import DashIconify

from controllers import cont_torrents as cont_t
from controllers import cont_files as cont_f

register_page(__name__, path="/torrents", icon="fa-solid:home")


def layout(l="n", **kwargs):
    # lazy load block
    if l == "n":
        return dmc.Container()
    else:
        service.log_printer(request.remote_addr, "torrents", "page opened")
        # all workers must be here!
        return dmc.Container(
            children=[
                html.Div(
                    [
                        cont_t.block_torrents(),
                        cont_t.add_torrent_modal(),
                        html.Div(id="torrent-notifications-container"),
                    ],
                ),
            ],
            pt=20,
            # style={"paddingTop": 20},
            className="dmc-container",
        )


@callback(
    [
        Output("modal-add-torrent", "opened"),
        Output("torrent-add", "n_clicks"),
        Output("torrent-start-download", "n_clicks"),
        Output("torrent-notifications-container", "children"),
    ],
    [
        Input("torrent-add", "n_clicks"),
        Input("torrent-start-download", "n_clicks"),
    ],
    State("modal-add-torrent", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks_add, n_clicks_upload, opened):
    if n_clicks_add > 0:
        source = "add"
        pass  # just open modal, not submitting
    elif n_clicks_upload > 0:
        source = "upload"
        pass  # upload torrent file and start download

    notif = dmc.Notification(
        title="Проверка кнопок",
        id="simple-notify",
        action="show",
        message=f"Нажата кнопка {source}",
        icon=DashIconify(icon="ic:round-celebration"),
    )

    return not opened, 0, 0, notif


@callback(
    Output("torrents-table-container", "children"), Input("torrent-update", "n_clicks")
)
def return_torrents_data(n):
    service.log_printer(request.remote_addr, "torrents", "toggle update")
    datatable = cont_t.get_torrents_data()
    # datatable = None
    return (
        cont_f.generate_html_table(
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
