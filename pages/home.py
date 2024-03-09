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
import dash_mantine_components as dmc
from flask import request
from datetime import datetime 
import shutil

register_page(__name__, path="/", icon="fa-solid:home")

def get_ring(drive, current_value, max_value, id: str, valid):
    percent = int(round(current_value/max_value, 2)*100)
    if valid == True:
        return dmc.Stack([
            dmc.RingProgress(
                            id=id,
                            sections=[{"value": percent, "color": "--bs-primary"}],
                            label=dmc.Center(dmc.Text(f"{str(percent)}%", color="--bs-primary", size=20)),
                            roundCaps=True,
                            size=130
            ),
            dmc.Text(f'{drive}: {current_value} GB / {max_value} GB')
        ], spacing=0, align='center')
    else:
        return dmc.Stack([
            dmc.RingProgress(
                            id=id,
                            sections=[{"value": 100, "color": "red"}],
                            label=dmc.Center(dmc.Text("NaN", color="--bs-primary", size=20)),
                            roundCaps=True,
                            size=130
            ),
            dcc.Markdown(f'Диск *{drive}* не обнаружен')
        ], spacing=0, align='center')

def get_drive_size(partition):
    try:
        partition_full = f'/mnt/{partition}/'
        total, used, _ = shutil.disk_usage(partition_full)

        total = total // (2**30)
        used = used // (2**30)
        valid = True
    except FileNotFoundError:
        total = 1
        used = 1
        valid = False

    return get_ring(partition, int(used), int(total), f'ring-{partition}', valid=valid)

def layout():
    lay = dmc.Container(
        children=[
            html.Div([
                html.H5('Свободное место на дисках', style={'text-align': 'center'}), 
                dmc.Group([
                    # get_ring('sdb1', 100, 300, 'idder'),
                    get_drive_size('sdb1'),
                    get_drive_size('sdc1'),
                    get_drive_size('sdd1'),
                ], position='center')
            ], className='block-background')
        ],
        pt=20,
        style={"paddingTop": 20},
    )
    now = datetime.now().strftime("%d/%b/%Y %H:%M:%S") 
    # print(f'{request.remote_addr} - - [{now}] | homepage {request.base_url}')
    print(f'{request.remote_addr} - - [{now}] | homepage')
    return lay