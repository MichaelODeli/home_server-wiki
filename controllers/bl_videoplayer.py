from dash import (
    html,
)
import dash_mantine_components as dmc
import dash_player as dp
import dash_bootstrap_components as dbc

def get_video_card(video_title, video_length, video_link):
    """
    Генерирует карточку для видео с заданными параметрами.

    Параметры:
    video_title (str): Название видео.
    video_length (str): Продолжительность видео.
    video_link (str): Ссылка на видео.

    Вывод:
    html.A: HTML-элемент <a> (гиперссылка), содержащий карточку для видео.
    """
    return html.A(
        [
            dbc.Card(
                children=[
                    dbc.CardImg(src="/assets/image-not-found.jpg", style={'height': '120px', 'object-fit': 'none', 'object-position': 'center'}
                    ),
                    dmc.Group(
                        [
                            dmc.Text(str(video_title), weight=500),
                            dbc.Badge(
                                str(video_length),
                                text_color="primary",
                                className="border me-1",
                                color="white",
                            ),
                        ],
                        position="apart",
                        mt="md",
                        mb="xs",
                        style={"padding": "0 10px 0 10px"}
                    ),
                ],
                # withBorder=True,
                # shadow="sm",
                # radius="md",
                style={"width": "auto"},  # prev: 350px
            )
        ],
        href=video_link,
        style={"text-decoration": "unset"},
    )