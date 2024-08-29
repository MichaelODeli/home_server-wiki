from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from controllers import db_connection, cont_header
from itertools import chain

# независимые компоненты
navbar_brand = html.A(
    "HomeServer",
    href="/",
    style={
        "textDecoration": "none",
        "height": "min-content",
        "color": "var(--bs-emphasis-color)",
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
        color="var(--bs-primary)",
        persistence_type="session",
        persistence=True,
    ),
    className="pt-sm-0",
)


# кнопки навбара
navbar_items_dict = cont_header.getHeaderLinks(conn=db_connection.getConn())
navbar_buttons = [
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
navbar_buttons_video = dmc.Menu(
    [
        dmc.MenuTarget(
            dbc.Button(
                "Ссылки ▾",
                outline=True,
                color="link",
                class_name="dropdown nav-item td-none no-box-shadow m-0",
            )
        ),
        dmc.MenuDropdown(dmc.Group(navbar_buttons), p="sm"),
    ]
)


# Блок для поисковой строки
def getSearchBar(search_target="/search", from_video=False):
    search_placeholder = "Поиск" if not from_video else "Поиск по видео"
    return html.Form(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Input(
                                name="query",
                                placeholder=search_placeholder,
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
        action=search_target,
        className="nav-item",
    )


# формирование навбаров для разных страниц сайта
def renderNavbar(from_video=False, from_search=False):
    search_bar = (
        (
            getSearchBar(search_target="/players/video/search", from_video=True)
            if from_video
            else getSearchBar()
        )
        if not from_search
        else None
    )
    navbar_items_mobile = dmc.Group(navbar_buttons + [search_bar])

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
                    span=2,
                    className="adaptive-hide",
                ),
                dmc.GridCol(
                    (search_bar),
                    span="auto",
                    className="adaptive-hide px-3",
                ),
                dmc.GridCol(
                    None,
                    span=2,
                    className="adaptive-hide",
                ),
                dmc.GridCol(
                    (navbar_buttons_video if from_video else dmc.Group(navbar_buttons)),
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
                    # className="adaptive-show block-background rounded",
                    className="adaptive-show p-2",
                    style={"background-color": "var(--bs-body-bg) !important"},
                ),
            ],
            w="100%",
            align="center",
        )
    ]
