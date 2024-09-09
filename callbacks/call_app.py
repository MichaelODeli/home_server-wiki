from dash import Input, Output, State, no_update, html, clientside_callback
from controllers import db_connection
from views import v_header
import dash_mantine_components as dmc


def getServerBlockerCallback(app):
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


def getNavbarCallbacks(app):
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


def getNavbarSearchBarCallbacks(app):
    @app.callback(
        Output("navbar-children", "children"),
        Input("url", "pathname"),
    )
    def headerFormat(pathname):
        if "/players/video" in pathname:
            if pathname == "/players/video/search":
                navbar_children = v_header.renderNavbar(
                    from_video=True, from_search=True
                )
            else:
                navbar_children = v_header.renderNavbar(from_video=True)
        elif pathname == "/search":
            navbar_children = v_header.renderNavbar(from_search=True)
        else:
            navbar_children = v_header.renderNavbar()

        return navbar_children


def getColorSwitchCallbacks(app):
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
        Output("mantine_theme", "forceColorScheme"),
        Input("color-mode-switch", "checked"),
    )
    def makeMantineTheme(value):
        return "dark" if value == True else "light"
