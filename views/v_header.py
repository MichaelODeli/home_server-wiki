from itertools import chain

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from controllers import cont_header, db_connection, service_controller

# независимые компоненты
navbar_brand = html.A(
    dmc.Title("MediaServer", order=3),
    href="/",
    style={
        "textDecoration": "none",
        "height": "min-content",
        "color": "var(--mantine-color-text)",
    },
    # className='navbar navbar-brand p-0 m-0'
)
theme_switch = html.Div(
    dmc.Switch(
        onLabel=DashIconify(icon="radix-icons:moon", width=20),
        offLabel=DashIconify(icon="radix-icons:sun", width=20),
        size="lg",
        id="color-mode-switch",
        className="nav-item",
        persistence_type="session",
        persistence=True,
    ),
    className="pt-sm-0",
)
navbar_user_dropdown = [
    dmc.Menu(
        [
            dmc.MenuTarget(
                dmc.Button(
                    dmc.Text("Привет, {nickname}!", fw=400),
                    variant="subtle",
                    rightSection=DashIconify(icon="gridicons:dropdown", width=20),
                    size="compact-sm",
                )
            ),
            dmc.MenuDropdown(
                [
                    dmc.MenuItem(
                        "Личный кабинет",
                        href="/account",
                    ),
                    dmc.MenuItem(
                        "Выйти",
                        href="/logout",
                    ),
                ],
                p="sm",
            ),
        ],
        trigger="hover",
    )
]


# кнопки навбара
navbar_items_dict = cont_header.get_header_links(conn=db_connection.get_conn())
navbar_buttons = [
    dmc.Menu(
        [
            dmc.MenuTarget(
                dmc.Button(
                    dmc.Text(header_group["header_group_name"], fw=400),
                    variant="subtle",
                    rightSection=DashIconify(icon="gridicons:dropdown", width=20),
                    size="compact-sm",
                )
            ),
            dmc.MenuDropdown(
                list(  # nested list for simple list
                    chain(
                        *[
                            [
                                dmc.MenuLabel(key),
                            ]  # header
                            + [
                                dmc.MenuItem(
                                    data["link_name"],
                                    href=data["link_href"],
                                )
                                for data in header_group["header_group_content"][
                                    key
                                ]  # data inside dict
                            ]
                            + [
                                dmc.MenuDivider(),
                            ]
                            for key in header_group["header_group_content"].keys()
                        ]
                    )
                )[:-1]
            ),
        ],
        trigger="hover",
    )
    for header_group in navbar_items_dict
] + navbar_user_dropdown

navbar_buttons_video = dmc.Menu(
    [
        dmc.MenuTarget(
            dmc.Button(
                dmc.Text("Ссылки", fw=400),
                variant="subtle",
                rightSection=DashIconify(icon="gridicons:dropdown", width=20),
                size="compact-sm",
            )
        ),
        dmc.MenuDropdown(dmc.Group(navbar_buttons, gap="xs"), p="sm"),
    ]
)


# Блок для поисковой строки
def get_search_bar(search_target="/search", from_video=False):
    """

    :param search_target:
    :param from_video:
    :return:
    """
    search_placeholder = "Поиск" if not from_video else "Поиск по видео"
    return html.Form(
        children=[
            dmc.Grid(
                [
                    dmc.GridCol(
                        [
                            dmc.TextInput(
                                name="query",
                                placeholder=search_placeholder,
                                rightSection=[
                                    service_controller.dmc_button_from_html(
                                        "Поиск", height="100%"
                                    )
                                ],
                                rightSectionWidth="max-content",
                                required=True,
                            ),
                            dmc.TextInput(display="none", value="y", name="l"),
                            dmc.TextInput(
                                display="none", value="y", name="auto_search"
                            ),
                        ],
                        span="auto",
                    ),
                ],
            )
        ],
        method="GET",
        action=search_target,
        className="nav-item",
    )


# формирование навбаров для разных страниц сайта
def render_navbar(from_video=False, from_search=False):
    """

    :param from_video:
    :param from_search:
    :return:
    """
    search_bar = (
        (
            get_search_bar(search_target="/players/video/search", from_video=True)
            if from_video
            else get_search_bar()
        )
        if not from_search
        else None
    )
    navbar_items_mobile = dmc.Group(navbar_buttons + [search_bar], gap="xs")

    return [
        dmc.Grid(
            [
                dmc.GridCol(
                    navbar_brand,
                    span="content",
                    className="d-flex justify-content-center align-items-center",
                ),
                dmc.GridCol(
                    None,
                    span=1,
                    className="adaptive-hide",
                ),
                dmc.GridCol(
                    search_bar,
                    span="auto",
                    className="adaptive-hide px-3",
                ),
                dmc.GridCol(
                    None,
                    span=1,
                    className="adaptive-hide",
                ),
                dmc.GridCol(
                    (
                        navbar_buttons_video
                        if from_video
                        else dmc.Group(navbar_buttons, gap="xs")
                    ),
                    span="content",
                    className="adaptive-hide",
                ),
                dmc.GridCol(span="auto", className="adaptive-show"),
                dmc.GridCol(theme_switch, span="content", className="col-height"),
                dmc.GridCol(
                    dmc.Burger(id="navbar-toggler"),
                    span="content",
                    className="adaptive-show",
                ),
                dbc.Collapse(
                    navbar_items_mobile,
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                    className="adaptive-show p-2",
                    # style={"background-color": "var(--mantine-color-body) !important"},
                ),
            ],
            w="100%",
            align="center",
        )
    ]
