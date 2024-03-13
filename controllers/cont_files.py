import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import (
    dcc,
    html
)
from random import randint as r
from dash_extensions import Purify

def nested_list_to_html(lst):
    """
    Рекурсивно преобразует вложенный список в маркированный список HTML.

    Параметры:
    lst (list): Вложенный список, который нужно преобразовать.

    Вывод:
    str: Строка, содержащая HTML-код маркированного списка.

    Для выделения текста жирным шрифтом, оберните текст в звездочки: *text*.
    """
    html = "<ul>\n"
    for item in lst:
        if isinstance(item, list):
            html += nested_list_to_html(item)
        else:
            if str(item)[0] == '*' and str(item)[-1] == '*':
                html += "<li><b>" + str(item)[1:-1] + "</b></li>\n"
            else:
                html += "<li>" + str(item) + "</li>\n"
    html += "</ul>\n"
    return html.replace('\n', '')


def generate_html_table(header: list, data: list):
    """
    Генерирует HTML-таблицу на основе переданных заголовков и данных.

    Параметры:
    header (list): Список заголовков столбцов таблицы.
    data (list): Список списков, представляющих строки данных таблицы.

    Вывод:
    html.Div: HTML-элемент div, содержащий таблицу.
    """
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


def block_files_list():
    return html.Div(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        html.H5("Менеджер файлов", style={"margin": "0"}),
                        span="content",
                    ),
                    dmc.Col(span="auto"),
                    dmc.ButtonGroup(
                        [
                            dmc.Button(
                                "Copy",
                                variant="outline",
                                disabled=True,
                            ),
                            dmc.Button(
                                "Move",
                                variant="outline",
                                disabled=True,
                            ),
                            dmc.Button(
                                "Remove",
                                variant="outline",
                                color="red",
                                disabled=True,
                            ),
                        ],
                        m="5px",
                    ),
                ],
                align="stretch",
                justify="center",
            ),
            dmc.Space(h=15),
            generate_html_table(
                ["Маркер", "Название файла", "Размер", "Дата добавления", "Действия"],
                [
                    [
                        DashIconify(icon="material-symbols:folder", width=20),
                        "Перейти в каталог выше",
                        None,
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                    [
                        dmc.Checkbox(id=f"checkbox-simple-{r(0, 100)}"),
                        "Какой-то важный файл",
                        "10 Мб",
                        "12-03-2024",
                        "e",
                    ],
                ],
            ),
        ],
        className="block-background",
    )


def tree_content(source):
    if source == "col":
        label = "Hello! This is on column!"
    elif source == "drawer":
        label = "Hello! This is on drawer!"
    else:
        raise ValueError
    
    return dmc.Stack([
        # label,
        Purify(nested_list_to_html(['C:/', ['Windows', ['System32', '*SysWOW64*'], 'Program Files', 'Program Files (x86)']]))
    ])


def get_drawer():
    return dmc.Drawer(
        children=[tree_content(source="drawer")],
        title=html.H5("Дерево папок"),
        id="drawer-tree",
        padding="md",
        zIndex=10000,
    )