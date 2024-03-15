import dash
from dash import dcc, html, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from dash_extensions import Purify

# css styles
icons_link = (
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css"
)
app = dash.Dash(
    __name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY, icons_link]
)

server = app.server
app.config.suppress_callback_exceptions = True


# function for generating Dash Iconify content
def get_icon(icon):
    """
    param:  \n
    `icon`: icon name
    """
    return dmc.ThemeIcon(
        DashIconify(icon=icon, width=18),
        size=30,
        radius=30,
        variant="subtle",
    )


# search bar HTML code
search_bar = Purify(
    """
        <form action="/search" method="GET" class="">
        <div class="g-0 ms-auto flex-nowrap mt-3 mt-md-0 align-items-center row">
            <div class="col"><input class="form-control" id="query" name="query" placeholder="Поиск по хранилищу"
                    step="any"></div>
            <input type="hidden" value="y" name="l" />
            <div class="col-auto"><button class="ms-2 btn btn-primary">Найти</button></div>
        </div>
    </form>"""
)

# ---- FORM NOT SUBMITTING ---
# search_bar2 = dbc.Form(
#     children=[
#         html.Div(
#             [
#                 html.Div(
#                     [
#                         dbc.Input(
#                             id="query",
#                             name="query",
#                             placeholder="Поиск по хранилищу",
#                             step="any",
#                         )
#                     ],
#                     className="col",
#                 ),
#                 dbc.Input(type="hidden", value="y", name="l"),
#                 html.Div(
#                     [dbc.Button("Найти", className="ms-2")],
#                     className="col-auto",
#                 ),
#             ],
#             className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 align-items-center row",
#         )
#     ],
#     className="",
#     method="GET",
#     action="/search",
# )

# navbar with buttons
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                "Home server",
                href="/",
                className="h3 header-text me-2",
                style={
                    "textDecoration": "none",
                    "color": "black",
                    "margin-bottom": "0px !important",
                },
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                children=[
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.DropdownMenu(
                                    label="Внешние утилиты",
                                    children=[
                                        dbc.DropdownMenuItem(
                                            "Настройка сервера", header=True
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Webmin", href="https://192.168.3.33:10000/"
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Параметры ПО", href="/settings?l=y"
                                        ),
                                        dbc.DropdownMenuItem(divider=True),
                                        dbc.DropdownMenuItem(
                                            "Торрент клиенты", header=True
                                        ),
                                        dbc.DropdownMenuItem(
                                            "qBittorrent",
                                            href="http://192.168.3.33:8124/",
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Transmission (obsolete)",
                                            href="http://192.168.3.33:12345/",
                                        ),
                                        dbc.DropdownMenuItem(divider=True),
                                        dbc.DropdownMenuItem(
                                            "Wiki-ресурсы", header=True
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Kiwix", href="http://192.168.3.33:789/"
                                        ),
                                    ],
                                    nav=True,
                                    in_navbar=True,
                                ),
                            ),
                            dbc.Col(
                                dbc.DropdownMenu(
                                    label="Медиа и файлы",
                                    children=[
                                        dbc.DropdownMenuItem("Плееры", header=True),
                                        dbc.DropdownMenuItem(
                                            "Видеоплеер",
                                            href="/players/videoplayer?l=y",
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Аудиоплеер",
                                            href="/players/audioplayer?l=y",
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Управление файлами", header=True
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Файловый менеджер",
                                            href="/files?l=y",
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Торрентокачалка",
                                            href="/torrents?l=y",
                                        ),
                                    ],
                                    nav=True,
                                    in_navbar=True,
                                ),
                            ),
                            dbc.Col(width="auto"),  # column for filling empty space
                        ],
                        className='custom-flex'
                    ),
                    search_bar,
                ],
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            )
        ]
    )
)


# Конструкция всего макета
app.layout = dmc.NotificationsProvider(html.Div(children=[navbar, dash.page_container]))


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=81)
