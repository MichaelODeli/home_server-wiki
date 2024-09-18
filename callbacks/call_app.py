from dash import Input, Output, State, no_update, html, clientside_callback
from controllers import db_connection
from views import v_header
import dash_mantine_components as dmc


def get_server_blocker_callback(app):
    """

    :param app: Flask app
    :return: callback
    """
    # standart callback for connection checking
    @app.callback(
        Output("server-avaliablity", "data"),
        Output("server-blocker", "children"),
        Input("mantine_theme", "style"),
        running=[
            (Output("loading-overlay", "visible"), True, False),
        ],
    )
    def server_blocker(style):
        """

        :param style: dummy
        :return:
        """
        if db_connection.test_conn():
            return True, no_update
        else:
            return False, html.Center(
                [dmc.Title("Сервис недоступен.", order=5)],
                style={"margin-top": "70px"},
            )


def get_navbar_callbacks(app):
    """

    :param app: Flask app
    :return: callback
    """
    # add callback for toggling the collapse on small screens
    @app.callback(
        Output("navbar-collapse", "is_open", allow_duplicate=True),
        # [Input("navbar-toggler", "n_clicks")],
        [Input("navbar-toggler", "opened")],
        [State("navbar-collapse", "is_open")],
        prevent_initial_call=True,
    )
    def toggle_navbar_collapse(n, is_open):
        """

        :param n:
        :param is_open:
        :return:
        """
        return n


def get_navbar_search_bar_callbacks(app):
    """

    :param app: Flask app
    :return: callback
    """
    @app.callback(
        Output("navbar-children", "children"),
        Input("url", "pathname"),
    )
    def header_format(pathname):
        """

        :param pathname:
        :return:
        """
        if "/players/video" in pathname:
            if pathname == "/players/video/search":
                navbar_children = v_header.render_navbar(
                    from_video=True, from_search=True
                )
            else:
                navbar_children = v_header.render_navbar(from_video=True)
        elif pathname == "/search":
            navbar_children = v_header.render_navbar(from_search=True)
        else:
            navbar_children = v_header.render_navbar()

        return navbar_children


def get_color_switch_callbacks(app):
    """

    :param app: Flask app
    :return: callback
    """
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
    def make_mantine_theme(value):
        """

        :param value:
        :return:
        """
        return "dark" if value else "light"
