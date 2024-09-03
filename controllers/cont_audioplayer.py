import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import dcc, html
import pandas as pd
from psycopg2.extensions import AsIs
from random import randint


def getAudioTypes(conn, type_id=None):
    with conn.cursor() as cursor:
        cursor.execute(
            """select * from (select distinct(type_id) from filestorage_mediafiles_summary fms where html_audio_ready)
                left join (select id as type_id, type_name from filestorage_types) ft using(type_id) %(addition)s;""",
            {"addition": AsIs(f"WHERE type_id = {type_id}" if type_id else "")},
        )

        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data


def getAudioDict(conn, type_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """select * from filestorage_mediafiles_summary fms WHERE html_audio_ready and type_id = %(type_id)s order by artist, audio_title;""",
            {"type_id": type_id},
        )

        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return data


