import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import dcc, html
from controllers import cont_files as cont_f
import qbittorrentapi
from datetime import datetime


def add_torrent_modal():
    loading_skeleton = dmc.Stack(
        gap="xs",
        children=[
            dmc.Skeleton(height=8, width="70%"),
            dmc.Skeleton(height=8),
            dmc.Skeleton(height=8),
            dmc.Skeleton(height=8, width="70%"),
        ],
    )
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
                            [
                                "Перетащите или ",
                                html.A(
                                    "выберите файлы",
                                    className="link-opacity-100",
                                    href="#",
                                ),
                            ]
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
                    dmc.Space(h=7),
                    html.H6("Информация о файле {filename}"),
                    loading_skeleton,
                    dmc.Space(h=7),
                    html.H6("Выберите категорию загружаемого файла"),
                    dmc.Select(
                        placeholder="Выберите",
                        id="torrent-category-select",
                        value="other",
                        data=[
                            {"value": "films", "label": "Фильмы"},
                            {"value": "apps", "label": "Программы"},
                            {"value": "serials", "label": "Сериалы"},
                            {"value": "other", "label": "Другое"},
                        ],
                        style={"width": "100%", "margin": "auto"},
                    ),
                    dbc.Button(
                        "Начать загрузку", id="torrent-start-download", n_clicks=0
                    ),
                ]
            )
        ],
    )


def bytes2human(n, format="%(value).1f %(symbol)s", symbols="customary"):
    """
    Convert n bytes into a human readable string based on format.
    symbols can be either "customary", "customary_ext", "iec" or "iec_ext",
    see: http://goo.gl/kTQMs

      >>> bytes2human(0)
      '0.0 B'
      >>> bytes2human(0.9)
      '0.0 B'
      >>> bytes2human(1)
      '1.0 B'
      >>> bytes2human(1.9)
      '1.0 B'
      >>> bytes2human(1024)
      '1.0 K'
      >>> bytes2human(1048576)
      '1.0 M'
      >>> bytes2human(1099511627776127398123789121)
      '909.5 Y'

      >>> bytes2human(9856, symbols="customary")
      '9.6 K'
      >>> bytes2human(9856, symbols="customary_ext")
      '9.6 kilo'
      >>> bytes2human(9856, symbols="iec")
      '9.6 Ki'
      >>> bytes2human(9856, symbols="iec_ext")
      '9.6 kibi'

      >>> bytes2human(10000, "%(value).1f %(symbol)s/sec")
      '9.8 K/sec'

      >>> # precision can be adjusted by playing with %f operator
      >>> bytes2human(10000, format="%(value).5f %(symbol)s")
      '9.76562 K'
    """
    SYMBOLS = {
        "customary": ("B", "K", "M", "G", "T", "P", "E", "Z", "Y"),
        "customary_ext": (
            "byte",
            "kilo",
            "mega",
            "giga",
            "tera",
            "peta",
            "exa",
            "zetta",
            "iotta",
        ),
        "iec": ("Bi", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi", "Yi"),
        "iec_ext": (
            "byte",
            "kibi",
            "mebi",
            "gibi",
            "tebi",
            "pebi",
            "exbi",
            "zebi",
            "yobi",
        ),
    }
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)


def decode_torrent_status(name):
    if name == "error":
        return "Ошибка"
    elif name == "missingFiles":
        return "Нет файлов"
    elif name == "uploading":
        return "[↑] Раздача"
    elif name == "pausedUP":
        return "[↑] Пауза"
    elif name == "queuedUP":
        return "[↑] В очереди"
    elif name == "stalledUP":
        return "[↑] Ожидание"
    elif name == "checkingUP":
        return "[↑] Проверка"
    elif name == "forcedUP":
        return "[П] Раздача"
    elif name == "allocating":
        return "[↓] Выделение места"
    elif name == "downloading":
        return "[↓] Загрузка"
    elif name == "metaDL":
        return "[↓] Проверка мета"
    elif name == "pausedDL":
        return "[↓] Пауза"
    elif name == "queuedDL":
        return "[↓] В очереди"
    elif name == "stalledDL":
        return "[↓] Ожидание"
    elif name == "checkingDL":
        return "[↓] Проверка"
    elif name == "forcedDL":
        return "[П] Загрузка"
    elif name == "checkingResumeData":
        return "[↓] Проверка"
    elif name == "moving":
        return "Перемещение"
    else:
        return "Неизвестно"


def get_torrents_data(qbittorrent_url="192.168.3.33:8124"):
    try:
        qbt_client = qbittorrentapi.Client(host=qbittorrent_url)
        torrents_data = []
        for torrent_info in qbt_client.torrents_info():
            t_hash = torrent_info["hash"]
            t_name = torrent_info["name"]
            t_progress = int(torrent_info["progress"] * 100)
            t_status = decode_torrent_status(torrent_info["state"])
            t_seeds = torrent_info["num_seeds"]
            t_speed_down = bytes2human(torrent_info["dlspeed"]) + "/s"
            t_speed_upl = bytes2human(torrent_info["upspeed"]) + "/s"
            t_added = datetime.fromtimestamp(torrent_info["added_on"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            t_completed = datetime.fromtimestamp(
                torrent_info["completion_on"]
            ).strftime("%Y-%m-%d %H:%M:%S")
            torrents_data.append(
                [
                    dmc.Checkbox(id=f"torrent-{t_hash}"),
                    t_name,
                    dmc.Progress(
                        value=t_progress, label=f"{str(t_progress)}%", size="xl"
                    ),
                    t_status,
                    t_seeds,
                    t_speed_down,
                    t_speed_upl,
                    t_added,
                    t_completed,
                ]
            )
        return torrents_data
    except:
        return None


def block_torrents():
    return html.Div(
        [
            dmc.Grid(
                [
                    dmc.GridCol(
                        html.H5("Управление торрентами", style={"margin": "0"}),
                        span="content",
                    ),
                    dmc.GridCol(span="auto"),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                DashIconify(icon="material-symbols:sync", width=25),
                                outline=True,
                                color="primary",
                                id="torrent-update",
                                className="button-center-content",
                                title="Обновить список",
                                # disabled=True,
                                size="md",
                                n_clicks=0,
                            ),
                            dbc.Button(
                                DashIconify(icon="material-symbols:add", width=25),
                                outline=True,
                                color="primary",
                                id="torrent-add",
                                className="button-center-content",
                                title="Добавить торрент",
                                disabled=True,
                                size="md",
                                n_clicks=0,
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
            dmc.Space(h=15),
            html.Div(id="torrents-table-container"),
        ],
        className="block-background",
    )
