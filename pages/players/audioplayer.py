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
import pandas as pd

register_page(__name__, path="/players/audioplayer", icon="fa-solid:home")

def get_playlist_button(name, href='https://example.com', content_type='Плейлист'):
    return html.A(dmc.Group([name, dbc.Badge(content_type, color='primary')]), href=href, style={'text-decoration': 'none'})

def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table

def layout(l = 'n', **kwargs):
    # lazy load block
    if l == 'n':
        return dmc.Container()
    else:
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S") 
        print(f'{request.remote_addr} - - [{now}] | audioplayer')
        df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

    return dmc.Container(
        children=[
            dbc.Row(children=[
                dbc.Col(lg=3, md=4, children=[
                    html.Div(style={'height': '100%'}, className='block-background-audio', children=[
                        dmc.Stack([
                            dbc.Button('Главная', outline=True, color='primary'),
                            dbc.Button('Поиск музыки', outline=True, color='primary'),
                            dmc.Divider(color='--bs-blue'),
                            get_playlist_button('Любимые треки'),
                            get_playlist_button('My favourite rock'),
                            get_playlist_button('AC/DC', content_type='Исполнитель'),
                            get_playlist_button('Рок', content_type='Жанр'),
                            get_playlist_button('Back in Black (AC/DC)', content_type='Альбом'),
                        ])
                    ]),
                ], className="mrrow phone-col"),
                dbc.Col(width=True, children=[
                    html.Div(style={'height': '500px', 'padding': '1%'}, className='block-background-audio', children=[
                        dmc.Stack([
                            html.H4('Плейлист: Мои любимые треки'),
                            dmc.Divider(color='--bs-blue'),
                            html.Div(dmc.Table(create_table(df)), className='table-wrapper'),
                        ])
                    ]),
                ], className="mrrow phone-col"),
            ],
            className="g-0",
            # style={'height': '500px'}
            )
        ],
        pt=20,
        # style={"paddingTop": 20},
        className='dmc-container',
        size="100%",
    )