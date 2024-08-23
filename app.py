import dash
from dash import dcc, html, Output, Input, State, clientside_callback, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from dash_extensions import Purify
from dash_extensions.pages import setup_page_components
from controllers import db_connection, cont_homepage

# from config import *
from dotenv import dotenv_values
import flask
import os
from itertools import chain

dash._dash_renderer._set_react_version("18.2.0")

# css styles
icons_link = [
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css"
]
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
        dbc.icons.FONT_AWESOME,
    ]
    + mantine_stylesheets
    + icons_link,
    # external_scripts=[
    #     "https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js",
    #     "https://cdnjs.cloudflare.com/ajax/libs/mediaelement/7.0.5/mediaelement-and-player.min.js",
    # ],
    title=config["WEB_PAGE_TITLE"],
    update_title=config["WEB_PAGE_LOADING_TITLE"],
    suppress_callback_exceptions=True,
)
app.config.suppress_callback_exceptions = True


# search bar HTML code
search_bar = html.Form(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(
                            id="search-bar-query",
                            name="query",
                            placeholder="Поиск по всем файлам",
                            step="any",
                        ),
                        dbc.Input(type="hidden", value="y", name="l"),
                        dbc.Input(type="hidden", value="y", name="auto_search"),
                    ]
                ),
                dbc.Col([dbc.Button("Найти", className="ms-2")], width="auto"),
            ],
        )
    ],
    method="GET",
    action="/search",
    className="nav-item",
    id="search-bar",
)

theme_switch = html.Div(
    dmc.Switch(
        offLabel=DashIconify(icon="radix-icons:moon", width=20),
        onLabel=DashIconify(icon="radix-icons:sun", width=20),
        size="lg",
        id="color-mode-switch",
        className="nav-item",
        color="var(--bs-primary)",
        label=dmc.Text(
            "Переключить тему приложения", className="adaptive-show p-0 m-0", size="sm"
        ),
        persistence_type='session',
        persistence=True
    ),
    className="pt-3 pt-sm-0",
)

navbar_items_dict = cont_homepage.getHeaderLinks(conn=db_connection.getConn())

navbar_items = dmc.Group(
    [
        dbc.DropdownMenu(
            label=header_group["header_group_name"],
            nav=True,
            in_navbar=True,
            children=list(  # nested list for simple list
                chain(
                    *[
                        [dbc.DropdownMenuItem(key, header=True)]  # header
                        + [
                            dbc.DropdownMenuItem(
                                data["link_name"],
                                href=data["link_href"],
                            )
                            for data in header_group["header_group_content"][
                                key
                            ]  # data inside dict
                        ]
                        + [
                            dbc.DropdownMenuItem(divider=True),
                        ]
                        for key in header_group["header_group_content"].keys()
                    ]
                )
            )[:-1],
        )
        for header_group in navbar_items_dict
    ]
    + [
        dmc.Space(h=3),
        search_bar,
        theme_switch,
    ]
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            dbc.NavbarBrand("HomeServer", className="ms-2"),
                            href="/",
                            style={"textDecoration": "none"},
                        ),
                    ),
                ],
                align="center",
                className="g-0",
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                navbar_items,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="default",
    class_name="rounded border-bottom",
)

# Конструкция всего макета
app.layout = dmc.MantineProvider(
    children=[
        dmc.Container(
            [
                navbar,
                dash.page_container,
                dmc.LoadingOverlay(
                    visible=True,
                    id="loading-overlay",
                    zIndex=1000,
                    overlayProps={"radius": "sm", "blur": 5},
                    loaderProps={"size": "lg"},
                ),
            ],
            miw="100%",
            mih="100%",
            id="server-blocker",
            p=0,
        ),
        dmc.NotificationProvider(position="bottom-right"),
        setup_page_components(),
        html.Div(id="notifications-container-search"),
        dcc.Store(id="server-avaliablity"),
        dcc.Location(id="url"),
        html.Div(id='dummy-1')
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


# standart callback for connection checking
@app.callback(
    Output("server-avaliablity", "data"),
    Output("server-blocker", "children"),
    Input("mantine_theme", "style"),
    running=[
        (Output("loading-overlay", "visible"), True, False),
    ],
)
def serverBlocker(style):
    if db_connection.testConn():
        return True, no_update
    else:
        return False, html.Center(
            [html.H5("Сервис недоступен. ")],
            style={"margin-top": "70px"},
        )


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggleNavbarCollapse(n, is_open):
    if n:
        return not is_open
    return is_open


# color theme switch
clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("dummy-1", "style"),
    Input("color-mode-switch", "checked"),
)


@app.callback(
    Output("mantine_theme", "forceColorScheme"), Input("color-mode-switch", "checked")
)
def makeMantineTheme(value):
    return "dark" if value == False else "light"


# search bar edits
@app.callback(
    Output("search-bar", "action"),
    Output("search-bar-query", "placeholder"),
    Input("url", "href"),
)
def searchBarFormat(href):
    if "/players/video" in href:
        return (
            "/players/video/search",
            "Поиск по видео",
        )
    else:
        return "/search", "Поиск по всем файлам"


dev = bool(config["APP_DEBUG_ENABLED"])

if __name__ == "__main__":
    if dev:
        app.run_server(
            debug=True, host=config["APP_HOST"], port=int(config["APP_PORT"])
        )
    else:
        from waitress import serve

        serve(app.server, host=config["APP_HOST"], port=int(config["APP_PORT"]))
