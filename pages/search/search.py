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

register_page(__name__, path="/search", icon="fa-solid:home")


def layout(query="", **other_unknown_query_strings):
    # print(query)
    if other_unknown_query_strings != {}:
        print(other_unknown_query_strings)
    return dmc.Container(
        children=[
            dmc.Space(h=10),
            dmc.Grid(
                children=[
                    # dmc.Col(span="auto"),
                    dmc.Col(
                        children=[
                            html.Div(
                                children=[
                                    html.H3("Поиск"),
                                    dmc.Space(h=10),
                                    dmc.Stack(
                                        children=[
                                            dmc.TextInput(
                                                label="Поисковый запрос",
                                                style={"width": "100%"},
                                                value=str(query),
                                                id='search_query'
                                            ),
                                            dmc.CheckboxGroup(
                                                label="Категории для поиска",
                                                orientation="horizontal",
                                                offset="md",
                                                mb=10,
                                                children=[
                                                    dmc.Checkbox(
                                                        label="YouTube",
                                                        value="category_YT",
                                                    ),
                                                    dmc.Checkbox(
                                                        label="Сериалы",
                                                        value="category_serials",
                                                        disabled=True,
                                                    ),
                                                    dmc.Checkbox(
                                                        label="Фильмы",
                                                        value="category_films",
                                                        disabled=True,
                                                    ),
                                                    dmc.Checkbox(
                                                        label="Программы",
                                                        value="category_apps",
                                                        disabled=True,
                                                    ),
                                                ],
                                                value=["category_YT"],
                                            ),
                                            # dmc.Space(h=3),
                                            dmc.CheckboxGroup(
                                                label="Поиск по...",
                                                orientation="horizontal",
                                                offset="md",
                                                mb=10,
                                                children=[
                                                    dmc.Checkbox(
                                                        label="Названию",
                                                        value="search_by_name",
                                                    ),
                                                    dmc.Checkbox(
                                                        label="Каналу / Категории",
                                                        value="search_by_category",
                                                        disabled=True,
                                                    ),
                                                ],
                                                value=["search_by_name"],
                                            ),
                                        ]
                                    ),
                                ],
                                className="block-background",
                            ),
                            dmc.Space(h=15),
                            html.Div(
                                children=[
                                    html.H3("Результаты поиска"),
                                    dmc.Space(h=10),
                                    'А их нет ¯\_(ツ)_/¯'
                                ],
                                className="block-background",
                                style={'width': '100%'}
                            ),
                            # dmc.Space(h=15),
                            # html.Div(
                            #     children=[],
                            #     className="block-background",
                            # ),
                        ],
                        # span=3,
                    ),
                    # dmc.Col(span="auto"),
                ]
            ),
        ],
        pt=20,
        style={"paddingTop": 20},
    )
