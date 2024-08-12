import dash
from dash import dcc, html, Output, Input, State, clientside_callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from dash_extensions import Purify
from dash_extensions.pages import setup_page_components

# from config import *
from dotenv import dotenv_values
import flask
import os

dash._dash_renderer._set_react_version("18.2.0")

# css styles
icons_link = (
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css"
)
mantine_stylesheets = [
    # dmc.styles.DATES,
    # dmc.styles.CODE_HIGHLIGHT,
    # dmc.styles.CHARTS,
    # dmc.styles.CAROUSEL,
    # dmc.styles.NOTIFICATIONS,
    "https://unpkg.com/@mantine/notifications@7.11.0/styles.css",
    # dmc.styles.NPROGRESS,
]

config = {
    **dotenv_values(".env"),  # load variables
    # **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

# flask and dash configuration
server = flask.Flask(config["APP_NAME"])
app = dash.Dash(
    config["APP_NAME"],
    server=server,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.ZEPHYR,
        "assets/offline/bootstrap.min.css",
    ]
    + mantine_stylesheets,
    title=config["WEB_PAGE_TITLE"],
    update_title=config["WEB_PAGE_LOADING_TITLE"],
    suppress_callback_exceptions=True,
)
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

# navbar with buttons
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.NavbarBrand(config["WEB_PAGE_HEADER_BRAND"], className="ms-2 h2"),
                href="/",
                style={"text-decoration": "unset"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                children=[
                    dmc.Grid(
                        [
                            dmc.GridCol(
                                [
                                    html.A("Новый поиск", href="/new_search?l=y"),
                                    dbc.DropdownMenu(
                                        label="Внешние утилиты",
                                        children=[
                                            dbc.DropdownMenuItem(
                                                "Настройка сервера",
                                                header=True,
                                                class_name="h6",
                                                style={"text-decoration": "unset"},
                                            ),
                                            dbc.DropdownMenuItem(
                                                "Webmin",
                                                href="https://192.168.3.33:10000/",
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
                                ],
                                span="content",
                            ),
                            dmc.GridCol(
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
                                            "Управление торрентом",
                                            href="/torrents?l=y",
                                        ),
                                    ],
                                    nav=True,
                                    in_navbar=True,
                                ),
                                span="content",
                            ),
                            dmc.GridCol(
                                [
                                    html.Span(
                                        [
                                            dbc.Label(
                                                className="fa fa-moon",
                                                html_for="color-mode-switch",
                                                color="primary",
                                            ),
                                            dbc.Switch(
                                                id="color-mode-switch",
                                                value=True,
                                                className="d-inline-block ms-1",
                                                persistence=True,
                                            ),
                                            dbc.Label(
                                                className="fa fa-sun",
                                                html_for="color-mode-switch",
                                                color="primary",
                                            ),
                                        ]
                                    )
                                ],
                                span="content",
                            ),
                            # dmc.GridCol(span="auto"),  # column for filling empty space
                        ],
                        className="custom-flex",
                    ),
                    html.Div(search_bar, style={"padding": "0 10px 0 10px"}),
                ],
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    style={"min-height": "80px"},
    class_name="rounded border-bottom",
    color="default",
)


# Конструкция всего макета
app.layout = dmc.MantineProvider(
    children=[
        navbar,
        dash.page_container,
        dmc.NotificationProvider(position="bottom-right"),
        setup_page_components(),
        html.Div(id="notifications-container-search"),
    ],
    id="mantine_theme",
    defaultColorScheme="light",
    theme={
        "primaryColor": "indigo",
        "fontFamily": 'system-ui, -apple-system, "Segoe UI", Roboto,'
        '"Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif,'
        '"Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol",'
        '"Noto Color Emoji"',
    },
)


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


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)


@app.callback(
    Output("mantine_theme", "forceColorScheme"), Input("color-mode-switch", "value")
)
def make_mantine_theme(value):
    return "dark" if value == False else "light"


dev = bool(config["APP_DEBUG_ENABLED"])

if __name__ == "__main__":
    if dev:
        app.run_server(
            debug=True, host=config["APP_HOST"], port=int(config["APP_PORT"])
        )
    else:
        from waitress import serve

        serve(app.server, host=config["APP_HOST"], port=int(config["APP_PORT"]))
