from dash import (
    html,
)
import dash_mantine_components as dmc
import dash_player as dp
import dash_bootstrap_components as dbc
from controllers import cont_media


def createVideoMiniatureContainer(
    href,
    video_title,
    videotype_name,
    views="нет просмотров",
    date="недавно",
    img_video="/assets/img/image-not-found.jpg",
    img_channel="/assets/img/image-not-found.jpg",
    video_duration=0,
):
    """
    Функция createVideoMiniaturesContainer создает контейнер для видео миниатюр.

    :param href (str): ссылка на видео.
    :param img_video (str): ссылка на изображение видео.
    :param img_channel (str): ссылка на изображение канала.
    :param video_title (str): заголовок видео.
    :param videotype_name (str): тип видео.
    :param views (str): количество просмотров.
    :param date (str): дата публикации.
    :return html.A: миниатюры видео.
    """
    return html.A(
        className="td-none",
        href=href,
        children=[
            dmc.Container(
                p=0,
                mt="xs",
                mb="sm",
                maw="300px",
                children=[
                    dmc.AspectRatio(
                        html.Div(
                            dmc.Text(
                                cont_media.getDuration(video_duration),
                                c="white",
                                bg="black",
                                w="max-content",
                                h="max-content",
                                className="video-time m-1 px-1",
                                size="sm",
                            )
                        ),
                        ratio=16 / 9,
                        mb="xs",
                        w=300,
                        className="video-background-image",
                        style={"background-image": f"url('{img_video}')"},
                    ),
                    dmc.Flex(
                        direction="row",
                        children=[
                            dmc.Avatar(radius="xl"),
                            dmc.Container(
                                children=[
                                    dmc.Text(
                                        video_title,
                                        td="none",
                                        fw=500,
                                        mb="5px",
                                        c="var(--bs-emphasis-color)",
                                    ),
                                    dmc.Text(videotype_name, c="gray", td="none"),
                                    dmc.Group(
                                        [
                                            dmc.Text(views, c="gray", td="none"),
                                            dmc.Text("•", c="gray", td="none"),
                                            dmc.Text(date, c="gray", td="none"),
                                        ],
                                        gap="xs",
                                    ),
                                ],
                                mt="3px",
                                ml="10px",
                                p=0,
                            ),
                        ],
                    ),
                ],
            )
        ],
    )


def createVideoMiniaturesContainer(children):
    """
    Функция createVideoMiniaturesContainer создает контейнер для видео миниатюр.

    :param children (tuple): наполнение контейнера
    :return dmc.Flex:
    """
    return dmc.Flex(
        direction="row",
        wrap="wrap",
        justify="space-around",
        mt="10px",
        mx="5px",
        children=children,
    )


def createVideoSearchBar(
    page, search_clicks=0, input_value=None, additional_children=[html.Div()]
):
    """
    Функция createVideoSearchBar создает строку поиска видео.

    :param page (object): экземпляр класса page.
    :param search_clicks (int): количество кликов по кнопке поиска.
    :param input_value (str): значение поля ввода.
    :param additional_children (list): список дополнительных дочерних элементов.

    :return dmc.Grid: экземпляр класса dmc.Grid с заданными параметрами и дочерними элементами.
    """

    search_form = dmc.Group(
        [
            dbc.Input(
                placeholder="Введите запрос",
                class_name="w-100",
                value=input_value,
                id="n_search_query_video",
                name="query",
            ),
            dbc.Input(type="hidden", value="y", name="l"),
            dbc.Input(type="hidden", value="y", name="auto_search"),
            dbc.Button(
                "Поиск",
                id="n_search_button_video",
                n_clicks=search_clicks,
            ),
        ],
        className="mx-2 mx-sm-0",
        justify="center",
        wrap="nowrap",
    )

    return dmc.Grid(
        [
            dmc.GridCol(span=3, className="adaptive-hide"),
            dmc.GridCol(
                span="auto",
                children=dmc.Stack(
                    [
                        (
                            html.Form(search_form, action="/players/video/search")
                            if page == "main"
                            else search_form
                        )
                    ]
                    + additional_children,
                    gap="xs",
                ),
            ),
            dmc.GridCol(span=3, className="adaptive-hide"),
        ],
        w="90%",
        m="auto",
    )


def getRandomVideos(conn, counter=30, type_id=None):
    if type_id != None:
        query = "select * from filestorage_mediafiles_summary where html_video_ready and type_id = %(type_id)s order by random() limit %(counter)s;"
    else:
        query = "select * from filestorage_mediafiles_summary where html_video_ready order by random() limit %(counter)s;"

    with conn.cursor() as cursor:
        cursor.execute(
            query,
            {"counter": counter, "type_id": type_id},
        )

        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data
