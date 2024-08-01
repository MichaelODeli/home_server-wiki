import dash_mantine_components as dmc
from dash_iconify import DashIconify
import time
import dash_bootstrap_components as dbc

videos_categories = [
    "cartoon_serials",
    "en_serials",
    "tv_shows",
    "youtube",
    "films",
    "ru_serials",
]

def get_icon(icon, size=18, background=True, icon_color="white"):
    """
    param:  \n
    `icon`: icon name
    """
    return (
        dmc.ThemeIcon(
            DashIconify(icon=icon, width=size, color=icon_color),
            size=size,
            radius=size + 7,
            # variant="subtle",
            color="#000000",
            m="5px",
        )
        if background == True
        else DashIconify(icon=icon, width=size, color=icon_color)
    )

def str_hider(name, limiter=25):
    """
    Сокращение строки до 30 символов, если не задано иное

    Параметры:
    ----------
    - name (str): сокращаемый текст
    - limiter (int): кол-во оставляемых символов (по умолчанию 30)
    """
    if len(name) <= limiter:
        return name
    else:
        return name[0:limiter] + "..."

def link_builder(server_link, name, hash, filetype, category, filename):
    """
    Генерация ссылок в файловом хранилище сервера

    Параметры:
    ----------
    - server_link - текущий адрес сервера
    - name - текст ссылки
    - hash - хэш файла на сервере
    - filetype - тип контента
    - category - категория контента
    - filename - название файла
    """
    return (
        dbc.Button(
            children=[
                (
                    get_icon("mdi:youtube")
                    if filetype == "youtube"
                    else get_icon("ic:movie")
                ),
                str_hider(name),
            ],
            style={"text-align": "center", "display": "flex", "align-items": "center"},
            outline=True,
            size="sm",
            href=f"/players/videoplayer?v={hash}&v_type={filetype}&l=y",
            className="link-primary",
        )
        if filetype in videos_categories and ".mp4" in filename
        else dbc.Button(
            children=[get_icon("ic:baseline-download"), str_hider(name)],
            style={"text-align": "center", "display": "flex", "align-items": "center"},
            outline=True,
            size="sm",
            href=f"http://{server_link}/storage/{filetype}/{category}/{filename}",
            download=filename,
            className="link-primary",
        )
    )

def search_link(filetype, category):
    """
    Получение ссылки на формирование поискового запроса

    Параметры:
    - filetype - тип файла
    - category - категория
    """
    return dbc.Button(
        children=[
            get_icon("mdi:youtube") if filetype == "youtube" else None,
            str_hider(category),
        ],
        style={"text-align": "center", "display": "flex", "align-items": "center"},
        outline=True,
        size="sm",
        href=f"/search?query={category}&from_video_view=True&l=y&search_category={filetype}",
        className="link-primary",
    )

def get_duration(seconds_data):
    """
    Преобразует количество секунд в формат времени HH:MM:SS.

    Параметры:
    seconds_data (float): Количество секунд.

    Вывод:
    str: Строка в формате HH:MM:SS, представляющая время.
    """
    if seconds_data < 3600: time_format = "%M:%S"
    else: time_format = "%H:%M:%S"
    return time.strftime(time_format, time.gmtime(float(seconds_data)))

def get_size_str(size):
    """
    Преобразует размер файла в удобочитаемый формат (МБ или ГБ).

    Параметры:
    size (float): Размер файла в байтах.

    Вывод:
    str: Строка, представляющая размер файла в МБ или ГБ.
    """
    size = float(size)
    if size <= 512:
        return str(size) + " MB"
    else:
        return str(round(size / 1024, 2)) + " GB"
