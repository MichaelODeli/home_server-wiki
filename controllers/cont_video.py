from dash import (
    html,
)
import dash_mantine_components as dmc
import dash_player as dp
import dash_bootstrap_components as dbc


def create_video_container(
    href, img_video, img_channel, video_title, videotype_name, views, date
):
    """
    Функция video_miniatures_container создает контейнер для видео миниатюр.

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
                        html.Img(src=img_video), ratio=16 / 9, mb="xs", w=300
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


def video_miniatures_container(children):
    """
    Функция video_miniatures_container создает контейнер для видео миниатюр.

    :param children (tuple): наполнение контейнера
    :return dmc.Flex:
    """
    return dmc.Flex(
        direction="row",
        wrap="wrap",
        justify="space-around",
        mt="20px",
        mx="5px",
        children=children,
    )


def video_search_bar(page, search_clicks=0, input_value=None, additional_children=[html.Div()]):
    """
    Функция video_search_bar создает строку поиска видео.

    :param page (object): экземпляр класса page.
    :param search_clicks (int): количество кликов по кнопке поиска.
    :param input_value (str): значение поля ввода.
    :param additional_children (list): список дополнительных дочерних элементов.

    :return dmc.Grid: экземпляр класса dmc.Grid с заданными параметрами и дочерними элементами.
    """
    return dmc.Grid(
        [
            dmc.GridCol(span=3, className="adaptive-hide"),
            dmc.GridCol(
                span="auto",
                children=dmc.Stack(
                    [
                        dmc.Group(
                            [
                                dbc.Input(
                                    placeholder="Введите запрос",
                                    class_name="w-100",
                                    value=input_value,
                                    id="n_search_query_video",
                                    name="search_query",
                                ),
                                dbc.Input(type="hidden", value="y", name="l"),
                                dbc.Input(
                                    type="hidden", value="y", name="auto_search"
                                ),
                                dbc.Button("Поиск", id='n_search_button_video', n_clicks=search_clicks),
                            ],
                            className="mx-2 mx-sm-0",
                            justify="center",
                            wrap="nowrap",
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
