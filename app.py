import dash
from dash import dcc, html, Output, Input, State, clientside_callback, no_update
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_extensions.pages import setup_page_components
from controllers import db_connection
from views import header

# from config import *
from dotenv import dotenv_values
import flask
import os


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
        dbc.icons.FONT_AWESOME,
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap"
    ]
    + mantine_stylesheets
    + icons_link,
    title=config["WEB_PAGE_TITLE"],
    update_title=config["WEB_PAGE_LOADING_TITLE"],
    suppress_callback_exceptions=True,
)


# Конструкция всего макета
app.layout = dmc.MantineProvider(
    children=[
        dmc.AppShell(
            [
                dmc.AppShellHeader(
                    children="",
                    id="navbar-children",
                    px=25,
                    py=10,
                    w="100dvw",
                    zIndex=100,
                ),
                dmc.AppShellMain(
                    [
                        dash.page_container,
                        dmc.LoadingOverlay(
                            visible=True,
                            id="loading-overlay",
                            zIndex=1000,
                            overlayProps={"radius": "sm", "blur": 5},
                            loaderProps={"size": "lg"},
                        ),
                    ],
                    id="server-blocker",
                ),
            ],
            # header={"height": {"sm": None, "md": 60}},
            header={"height": 60},
            id="appshell-props",
        ),
        dmc.NotificationProvider(position="bottom-right"),
        setup_page_components(),
        html.Div(id="notifications-container-search"),
        dcc.Store(id="server-avaliablity"),
        dcc.Location(id="url-audio"),
        dcc.Location(id="url"),
        html.Div(id="dummy-1"),
    ],
    id="mantine_theme",
    defaultColorScheme="light",
    theme={
        # "primaryColor": "indigo",
        "primaryColor": "custom-blue",
        "fontFamily": """Inter, -apple-system, BlinkMacSystemFont, 
            "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, 
            "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol" """,
        "headings": {
            "fontFamily": """Inter, -apple-system, BlinkMacSystemFont, 
                "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, 
                "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol" """,
            "fontWeight": 500,
        },
        "colors": {
            "custom-blue": [
                '#eef3ff',
                '#dce4f5',
                '#b9c7e2',
                '#94a8d0',
                '#748dc1',
                '#5f7cb8',
                '#5474b4',
                '#44639f',
                '#39588f',
                '#2d4b81'
            ]
        },
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
            [dmc.Title("Сервис недоступен.", order=5)],
            style={"margin-top": "70px"},
        )


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open", allow_duplicate=True),
    # [Input("navbar-toggler", "n_clicks")],
    [Input("navbar-toggler", "opened")],
    [State("navbar-collapse", "is_open")],
    prevent_initial_call=True,
)
def toggleNavbarCollapse(n, is_open):
    return n


# color theme switch
clientside_callback(
    """
    (switchOn) => {
       switchOn = !switchOn
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark"); 
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
    return "dark" if value == True else "light"


@app.callback(
    Output("navbar-children", "children"),
    Input("url", "pathname"),
)
def headerFormat(pathname):
    if "/players/video" in pathname:
        if pathname == "/players/video/search":
            navbar_children = header.renderNavbar(from_video=True, from_search=True)
        else:
            navbar_children = header.renderNavbar(from_video=True)
    elif pathname == "/search":
        navbar_children = header.renderNavbar(from_search=True)
    else:
        navbar_children = header.renderNavbar()

    return navbar_children


dev = bool(config["APP_DEBUG_ENABLED"])

if __name__ == "__main__":
    if dev:
        app.run(
            debug=True,
            host=config["APP_HOST"],
            port=int(config["APP_PORT"]),
            dev_tools_props_check=False,
        )
    else:
        from waitress import serve

        serve(app.server, host=config["APP_HOST"], port=int(config["APP_PORT"]))
