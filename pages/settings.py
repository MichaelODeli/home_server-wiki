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
import dash_bootstrap_components as dbc
from dash_extensions import Purify

register_page(__name__, path="/settings", icon="fa-solid:home")

checker_layout = dmc.Stepper(
            id="stepper",
            active=0,
            breakpoint="sm",
            children=[
                dmc.StepperStep(
                    label="Интернет",
                    description="ping: ...",
                    loading=True,
                    color='var(--bs-danger)'
                ),
                dmc.StepperStep(
                    label="VPN",
                    description="Результат: ...",
                    loading=True,
                    color='var(--bs-primary)'
                ),
                dmc.StepperStep(
                    label="Температура системы",
                    description="Результат: ...",
                    loading=True,
                    color='var(--bs-primary)'
                ),
                dmc.StepperStep(
                    label="Работа приложений",
                    description="Результат: ...",
                    loading=True,
                    color='var(--bs-primary)'
                ),
            ],
        )

def layout(): 
    global checker_layout
    return dmc.Container(
        children=[
            dmc.Space(h=10),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Основные настройки", value="main"),
                            dmc.Tab("Настройки сервера", value="server"),
                            dmc.Tab("Обработчик файлов", value="files"),
                        ],
                        grow=True
                    ),
                    dmc.TabsPanel(children=[
                        dmc.Space(h=5),
                        dmc.Stack(
                            children=[
                                # dmc.TextInput(label="Какое-то поле ввода"),
                            ],
                        )
                    ], value="main"),
                    dmc.TabsPanel(children=[
                        dmc.Space(h=5),
                        dmc.Stack([
                            html.H5('Проверка показателей сервера'),
                            dbc.Button('Запустить проверку'),
                            checker_layout,
                            dmc.Divider(variant="solid"),
                            html.H5('Кнопки управления сервером'),
                            dmc.TextInput(label="Кодовая фраза", style={"width": 250},),
                            dbc.ButtonGroup(
                                [dbc.Button("Перезагрузка сервера"), dbc.Button("Перезагрузка приложения"), dbc.Button("Выключение сервера")]
                            )
                        ])
                    ], value="server"),
                    dmc.TabsPanel(children=[
                        dmc.Space(h=5),
                        dmc.Stack(
                            children=[
                                html.H5('Каталоги'),
                                dmc.TextInput(label="Родительский каталог с файлами", style={"width": 250},),
                                dmc.Divider(variant="solid"),
                                html.H5('Обновление библиотеки'),
                                dmc.NumberInput(
                                    label="Интервал обновления базы",
                                    description="Указана периодичность в днях",
                                    value=1,
                                    min=1,
                                    style={"width": 250},
                                ),
                                dmc.Divider(variant="solid"),
                                html.H5('Категории'),
                                dmc.MultiSelect(
                                    label="Обнаруженные категории файлов",
                                    description='Категорией служит название подпапки в родительской папке с файлами',
                                    value=["youtube", "films"],
                                    data=['history', 'cartoon_serials', 'en_serials', 'data_science', 'apps', 'books', 'tv_shows', 'youtube', 'films', 'wiki'],
                                    style={"width": 400, "marginBottom": 10},
                                ),
                                dbc.Button('Обновить библиотеку по выбранным категориям'),
                                dbc.Button('Сбросить индексацию и обновить библиотеку'),
                                dmc.Divider(variant="solid"),
                                html.H5('Кнопки управления'),
                                dbc.Button('Принудительно обновить библиотеку файлов'),
                                dbc.Button('Отключить файлового менеджера'),
                                dmc.Divider(variant="solid"),
                                html.H5('Лог обновления базы'),
                                dbc.Button('Получить лог'),
                            ],
                        )
                    ], value="files"),
                ],
                variant="outline",
                orientation="horizontal",
                className='block-background',
                style={'height': '100%', 'width': '100%'}
            )
        ],
        pt=20,
        style={"paddingTop": 20, 'width': '100%'},
    )