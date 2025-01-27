import dash_mantine_components as dmc
from dash import (register_page)
# from flask_login import current_user

register_page(
    __name__,
    path="/account",
)

# USERDATA = ""


def layout(l="y", **kwargs):  # noqa: E741
    """

    :param l:
    :param kwargs:
    :return:
    """
    # global USERDATA

    # if not current_user.is_authenticated or l == "y" or not db_connection.test_conn():
    #     return html.Div()
    # else:
    #     username = current_user.get_id()
    #     USERDATA = users_controllers.get_user_info(username=username)

    return dmc.Grid(
        [
            dmc.GridCol(className="adaptive-hide", span=1),
            dmc.GridCol(
                children=dmc.Card(
                    [
                        dmc.Stack(
                            [
                                dmc.Avatar(size="xl"),
                                dmc.Text("{nickname}", fw=500),
                                dmc.Text("{access_level}", c="gray"),
                            ],
                            align="center",
                            w="100%",
                            gap="xs",
                        )
                    ],
                    shadow="sm",
                    radius="md",
                    withBorder=True,
                ),
                span=3,
                className="m-1 p-1 adaptive-width",
            ),
            dmc.GridCol(
                className="m-1 p-1 adaptive-width",
            ),
            dmc.GridCol(className="adaptive-hide", span=1),
        ],
        style={"paddingTop": "6dvh"},
        className="adaptive-block",
        maw='99%'
    )
