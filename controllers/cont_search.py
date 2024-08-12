import dash_mantine_components as dmc
from dash_iconify import DashIconify
import time
from dash import html
import dash_bootstrap_components as dbc


def get_icon(icon, size=18, background=True, icon_color="white"):
    """
    Функция get_icon возвращает иконку с заданными параметрами.

    :param icon: имя иконки
    :param size: размер иконки
    :param background: флаг, указывающий на необходимость отображения фона у иконки
    :param icon_color: цвет иконки
    :return: иконка с заданными параметрами
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


def str_hider(name, limiter=35):
    """
    Функция str_hider сокращает строку до заданного лимита символов.

    :param name: сокращаемый текст
    :param limiter: количество оставляемых символов (по умолчанию 35)
    :return: сокращенная строка
    """
    if len(name) <= limiter:
        return name
    else:
        return name[0:limiter] + "..."


def link_builder(mode, file_dict):
    """
    Функция link_builder создает ссылку на файл в зависимости от заданного режима.

    :param mode: режим, определяющий, как будет создана ссылка
    :param file_dict: словарь с информацией о файле
    :return: ссылка на файл
    """
    file_href = "http://" + file_dict["file_fullway_forweb"]

    if mode == "open_mediafiles_in_internal_player" and file_dict["html_video_ready"]:
        file_href = f"/players/videoplayer?v={file_dict['file_id']}&l=y"
    elif mode == "open_mediafiles_in_vlc" and file_dict["mime_type"].split("/")[0] in [
        "video",
        "audio",
    ]:
        file_href = "vlc://" + file_dict["file_fullway_forweb"]
    else:
        pass

    return html.A(
        str_hider(file_dict["file_name"]),
        href=file_href,
        target='_blank'
    )


def search_link(category_id, type_id):
    """
    Получение ссылки на формирование поискового запроса по категории и типу

    Параметры:
    - filetype - тип файла
    - category - категория
    """
    return html.A(
        children=[
            # get_icon("mdi:youtube") if filetype == "youtube" else None,
            get_icon("mdi:youtube"),
            str_hider(category_id),
        ],
        style={"text-align": "center", "display": "flex", "align-items": "center"},
        outline=True,
        size="sm",
        href=f"/search?auto_search=y&l=y&category_id={category_id}&type_id={type_id}",
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
    if seconds_data < 3600:
        time_format = "%M:%S"
    else:
        time_format = "%H:%M:%S"
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
