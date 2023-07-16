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
import sqlite3

register_page(__name__, path="/search", icon="fa-solid:home")


def layout(query="", from_video_view='False', **other_unknown_query_strings):
    if from_video_view == 'False': value_for_radio = 'search_by_name'
    else: value_for_radio = 'search_by_category'

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
                                            dmc.RadioGroup(
                                                label="Категории для поиска",
                                                orientation="horizontal",
                                                offset="md",
                                                mb=10,
                                                children=[
                                                    dmc.Radio(
                                                        label="YouTube",
                                                        value="category_YT",
                                                    ),
                                                    dmc.Radio(
                                                        label="Сериалы",
                                                        value="category_serials",
                                                        # disabled=True,
                                                    ),
                                                    dmc.Radio(
                                                        label="Фильмы",
                                                        value="category_films",
                                                        # disabled=True,
                                                    ),
                                                    dmc.Radio(
                                                        label="Программы",
                                                        value="category_apps",
                                                        # disabled=True,
                                                    ),
                                                ],
                                                value="category_YT",
                                            ),
                                            # dmc.Space(h=3),
                                            dmc.RadioGroup(
                                                label="Поиск по...",
                                                orientation="horizontal",
                                                offset="md",
                                                mb=10,
                                                id='search_by',
                                                children=[
                                                    dmc.Radio(
                                                        label="Названию",
                                                        value="search_by_name",
                                                    ),
                                                    dmc.Radio(
                                                        label="Каналу / Категории",
                                                        value="search_by_category",
                                                    ),
                                                ],
                                                value=value_for_radio,
                                            ),
                                            dmc.Space(h=3),
                                            dmc.Button("Поиск", id='search_button'),
                                        ]
                                    ),
                                ],
                                className="block-background",
                                style={'width': '100%'}
                            ),
                            dmc.Space(h=15),
                            html.Div(
                                children=[
                                    html.H3("Результаты поиска"),
                                    dmc.Space(h=10),
                                    html.Div(id='table_search'),
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

@callback(
    [
        Output("table_search", "children"),
    ],
    [
        State("search_by", "value"),
        State("search_query", 'value'),
    ],
    [
        Input("search_button", "n_clicks")
    ],
    prevent_initial_call=False,
)
def table_results(search_by, search_query, n_clicks):
    if search_query == '': 
        return 'А их нет ¯\_(ツ)_/¯'
    else:
        def str_hider(name):
            limiter = 30
            if len(name) <= limiter:
                return name
            else: return name[0:limiter]+'...'

        def name_builder(name, hash):
            return html.A(str_hider(name), href=f'/players/videoplayer?v={hash}')

        filetype = 'youtube'
        if search_by == 'search_by_category': 
            column = 'type'
        else:
            column = 'filename'

        conn = sqlite3.connect('bases/nstorage.sqlite3')
        c = conn.cursor()
        c.execute(f"SELECT * FROM {filetype} WHERE {column} LIKE '%{search_query}%'")
        results = c.fetchall()

        table_header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Источник"),
                        html.Th("Канал / Категория"),
                        html.Th("Название"),
                    ]
                )
            )
        ]

        table_content = []
        for result_line in results:
            category = result_line[1]
            filename = result_line[2]
            name = '.'.join(filename.split('.')[:-1])
            table_content += [html.Tr([html.Td(filetype),html.Td(str_hider(category)),html.Td(name_builder(name, result_line[0])),])]

        table_content = [html.Tbody(table_content)]

        c.close()
        conn.close()

        return [dmc.Table(table_header + table_content)]