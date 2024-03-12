import dash_mantine_components as dmc
from dash_iconify import DashIconify


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