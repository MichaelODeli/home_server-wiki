from dash import (
    html,
)
import dash_mantine_components as dmc
import dash_player as dp
import dash_bootstrap_components as dbc

def get_video_card(video_title, video_length, video_link):
    return html.A(
        [
            dmc.Card(
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
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                style={"width": "auto"},  # prev: 350px
            )
        ],
        href=video_link,
    )