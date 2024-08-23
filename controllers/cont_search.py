from dash import html, callback, Output, Input, State, no_update
import dash_mantine_components as dmc

from controllers import file_manager, db_connection

PAGE_LIMIT = 18


def stringHider(name, limiter=35):
    """
    Функция stringHider сокращает строку до заданного лимита символов.

    :param name: сокращаемый текст
    :param limiter: количество оставляемых символов (по умолчанию 35)
    :return: сокращенная строка
    """
    if len(name) <= limiter:
        return name
    else:
        return name[0:limiter] + "..."


def getLinkToFile(mode, file_dict):
    """
    Функция getLinkToFile создает ссылку на файл в зависимости от заданного режима.

    :param mode: режим, определяющий, как будет создана ссылка
    :param file_dict: словарь с информацией о файле
    :return: ссылка на файл
    """
    file_href = "http://" + file_dict["file_fullway_forweb"]

    if mode == "open_mediafiles_in_internal_player" and file_dict["html_video_ready"]:
        file_href = f"/players/video/watch?v={file_dict['file_id']}&l=y"
    elif mode == "open_mediafiles_in_vlc" and file_dict["mime_type"].split("/")[0] in [
        "video",
        "audio",
    ]:
        file_href = "vlc://" + file_dict["file_fullway_forweb"]
    else:
        pass

    return html.A(stringHider(file_dict["file_name"]), href=file_href, target="_blank")


def formatSearchResults(query_results, mediafiles_links_format):
    """
    Функция formatSearchResults форматирует результаты поиска.

    :param query_results (list): список результатов поиска.
    :param mediafiles_links_format (str): формат ссылки на медиафайл.

    :return dmc.Table: экземпляр класса dmc.Table с заданными параметрами и дочерними элементами.
    """
    rows = [
        dmc.TableTr(
            [
                dmc.TableTd(element["category_name"]),
                dmc.TableTd(element["type_name"]),
                dmc.TableTd(getLinkToFile(mediafiles_links_format, element)),
            ]
        )
        for element in query_results
    ]

    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Категория", className="sticky-th"),
                dmc.TableTh("Тип", className="sticky-th"),
                dmc.TableTh("Файл", className="sticky-th"),
            ]
        )
    )
    body = dmc.TableTbody(rows)

    return dmc.Table([head, body])


def getSearchAccordion(category_id, type_id, category_select_data, from_video=False):
    """
    Функция getSearchAccordion создает аккордеон для поиска.

    :param category_id (list): идентификатор категории.
    :param type_id (list): идентификатор типа.
    :param category_select_data (list_of_dicts): список данных для выбора категории.
    :param from_video (bool): флаг, указывающий на запуск со страницы с видео.

    :return dmc.Accordion: экземпляр класса dmc.Accordion с заданными параметрами и дочерними элементами.
    """
    return dmc.Accordion(
        variant="filled",
        chevronPosition="left",
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(
                        dmc.Text(
                            "Дополнительные параметры",
                            c="var(--bs-body-color)",
                        )
                    ),
                    dmc.AccordionPanel(
                        [
                            dmc.Divider(
                                label="Фильтры для поиска",
                                labelPosition="left",
                                h="lg",
                            ),
                            dmc.Grid(
                                [
                                    dmc.GridCol(
                                        [
                                            dmc.MultiSelect(
                                                w="100%",
                                                searchable=True,
                                                hidePickedOptions=True,
                                                clearable=True,
                                                label="Категория для поиска",
                                                id="n_search_in_category"
                                                + ("_video" if from_video else ""),
                                                placeholder="Поиск по всем категориям",
                                                data=category_select_data,
                                                value=category_id,
                                            )
                                        ],
                                        span=6,
                                        className="adaptive-container",
                                    ),
                                    dmc.GridCol(
                                        [
                                            dmc.MultiSelect(
                                                w="100%",
                                                searchable=True,
                                                hidePickedOptions=True,
                                                clearable=True,
                                                label="Типы для поиска",
                                                id="n_search_in_types"
                                                + ("_video" if from_video else ""),
                                                placeholder="Поиск по всем типам",
                                                disabled=True,
                                                value=type_id,
                                            )
                                        ],
                                        span=6,
                                        className="adaptive-container",
                                    ),
                                ],
                                w="100%",
                                justify="center",
                                className="adaptive-block",
                            ),
                            dmc.Space(h="md"),
                            (
                                dmc.Divider(
                                    label="Опции для отображения результатов",
                                    labelPosition="left",
                                    h="md",
                                )
                                if not from_video
                                else html.Div()
                            ),
                            dmc.Space(h="md") if not from_video else html.Div(),
                            (
                                dmc.RadioGroup(
                                    dmc.Stack(
                                        [
                                            dmc.Radio(
                                                label="Открывать поддерживаемые "
                                                "медиафайлы во встроенном плеере",
                                                value="open_mediafiles_in_internal_player",
                                            ),
                                            dmc.Radio(
                                                label="Открывать медиафайлы в VLC "
                                                "(mobile)",
                                                value="open_mediafiles_in_vlc",
                                            ),
                                            dmc.Radio(
                                                label="Стандартные прямые ссылки",
                                                value="full_links",
                                            ),
                                        ],
                                        gap="xs",
                                    ),
                                    value=(
                                        "full_links"
                                        if not from_video
                                        else "open_mediafiles_in_internal_player"
                                    ),
                                    id="mediafiles_links_format",
                                )
                                if not from_video
                                else html.Div()
                            ),
                        ]
                    ),
                ],
                value="info",
            ),
        ],
    )


def formatCategoryType(category_id, type_id):
    """
    Функция formatCategoryType форматирует идентификаторы категории и типа.

    :param category_id (list): список идентификаторов категории.
    :param type_id (list): список идентификаторов типа.

    :return tuple: кортеж из двух списков идентификаторов категории и типа.
    """
    category_id = [category_id] if category_id != [] else category_id
    type_id = [type_id] if type_id != [] else type_id
    return category_id, type_id


def getTypesAdditionFormatCallback(from_video=False):
    @callback(
        Output("n_search_in_types" + ("_video" if from_video else ""), "data"),
        Output("n_search_in_types" + ("_video" if from_video else ""), "disabled"),
        Output(
            "n_search_in_category" + ("_video" if from_video else ""), "placeholder"
        ),
        Output("n_search_in_types" + ("_video" if from_video else ""), "placeholder"),
        Input("n_search_in_category" + ("_video" if from_video else ""), "value"),
        State("n_search_in_types" + ("_video" if from_video else ""), "value"),
    )
    def addTypesInSearch(category_id, selected_types):
        if category_id == None or category_id == []:
            return no_update, True, "Поиск по всем категориям", "Поиск по всем типам"
        else:
            conn = db_connection.getConn()

            types_select_data = []

            for single_c_id in category_id:
                single_c_id = int(single_c_id)
                found_category = file_manager.getCategories(
                    conn, category_id=single_c_id
                )

                c_data = []

                if len(found_category) > 0:
                    found_types = len(
                        file_manager.getTypes(conn, category_id=single_c_id)
                    )
                    if found_types > 0:
                        c_data += [
                            {
                                "label": (
                                    i["type_pseudonym"]
                                    if i["type_pseudonym"] != None
                                    else i["type_name"]
                                ),
                                "value": str(i["type_id"]),
                            }
                            for i in file_manager.getTypes(
                                conn, category_id=single_c_id
                            )
                        ]

                        types_select_data += [
                            {
                                "group": found_category[0]["category_name"],
                                "items": c_data,
                            }
                        ]

            return (
                types_select_data,
                False,
                "Поиск по выбранным категориям",
                (
                    "Поиск по выбранным типам"
                    if len(selected_types) > 0
                    else "Поиск по всем типам"
                ),
            )


def getSearchResults(conn, query, categories, types, limit, offset, from_video=False):
    """
    Функция getSearchResults получает результаты поиска.

    :param conn (object): соединение с базой данных.
    :param query (str): запрос поиска.
    :param categories (list): список идентификаторов категории.
    :param types (list): список идентификаторов типа.
    :param limit (int): ограничение на количество результатов.
    :param offset (int): смещение для пагинации.
    :param from_video (bool): флаг, указывающий на видео.

    :return tuple: кортеж из двух элементов - счетчика результатов и списка результатов поиска.
    """
    if (query == None or query == "") and (
        categories == [] or (categories == [] and types == [])
    ):
        counter = -1
        query_results = -1
    elif (query != None and query != "") and (categories == [] and types == []):
        counter, query_results = file_manager.getFilesearchResult(
            conn,
            mode="all",
            query=query,
            limit=limit,
            offset=offset,
            from_video=from_video,
        )
    elif (query != None and query != "") and (categories != [] and types == []):
        counter, query_results = file_manager.getFilesearchResult(
            conn,
            mode="by_category",
            query=query,
            categories=categories,
            limit=limit,
            offset=offset,
            from_video=from_video,
        )
    elif (query == None or query == "") and (categories != [] and types == []):
        counter, query_results = file_manager.getFilesearchResult(
            conn,
            mode="all_from_category",
            categories=categories,
            limit=limit,
            offset=offset,
            from_video=from_video,
        )
    elif (query == None or query == "") and (categories != [] and types != []):
        counter, query_results = file_manager.getFilesearchResult(
            conn,
            mode="all_from_category_type",
            categories=categories,
            types=types,
            limit=limit,
            offset=offset,
            from_video=from_video,
        )
    elif (query != None and query != "") and (categories != [] and types != []):
        counter, query_results = file_manager.getFilesearchResult(
            conn,
            mode="by_category_type_query",
            query=query,
            categories=categories,
            types=types,
            limit=limit,
            offset=offset,
            from_video=from_video,
        )
    else:
        counter = -2
        query_results = -2

    return counter, query_results


def getCategoriesForMultiSelect(conn, video=False):
    category_select_data = [
        {
            "label": (
                i["category_pseudonym"]
                if i["category_pseudonym"] != None
                else i["category_name"]
            ),
            "value": str(i["category_id"]),
        }
        for i in file_manager.getCategories(conn)
        if i["main_mime_type_id"] == 9 and video
    ]

    return category_select_data
