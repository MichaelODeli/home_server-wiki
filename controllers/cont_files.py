import dash_mantine_components as dmc
from dash_iconify import DashIconify
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


def get_button_with_tooltip(
    button_id, icon_name, tooltip_text, tooltip_position="bottom"
):
    return dmc.Tooltip(
        label=tooltip_text,
        position=tooltip_position,
        offset=3,
        withArrow=True,
        children=[
            dmc.ActionIcon(
                DashIconify(icon=icon_name, width=20), size="lg", id=button_id
            )
        ],
    )


def generate_html_table(header: list, data: list):
    header = [
        html.Thead(html.Tr([html.Th(header_element) for header_element in header]))
    ]
    body = [
        html.Tbody(
            [html.Tr([html.Td(value) for value in row_data]) for row_data in data]
        )
    ]

    return html.Div(
        [dmc.Table(header + body)],
        style={"overflow-x": "auto", "white-space": "nowrap"},
    )
