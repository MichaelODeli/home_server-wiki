try:
    from controllers import db_connection
except ImportError:
    import db_connection

import os
import uuid
import mimetypes


def defineMIMEType(conn, fileway):
    mime = mimetypes.guess_type(fileway)
    if mime[0] == None:
        with conn.cursor() as cursor:
            cursor.execute(f"select type_name from mime_types_secondary mts where extension like '%{fileway.split('.')[-1]}%';")
            result = cursor.fetchone()
            return result[0] if result != None else 'unknown/unknown'
    else:
        return mime[0]


def getMediaInfo():
    return NotImplementedError

# вставка
def insertMIME(mime_name, conn) -> dict:
    """
    Функция insertMIME принимает на вход имя MIME-типа и возвращает его описание.
    Если запись с таким именем MIME-типа отсутствует в базе данных, она создает новую запись.
    В противном случае функция возвращает уже существующую запись.

    :param mime_name: имя MIME-типа
    :param conn: соединение с базой данных
    :return: описание MIME-типа:
    {secondary_mime_id, primary_mime_id, type_name, is_audio, is_video, html_video_ready, html_audio_ready, search_enabled}
    """
    # conn = db_connection.get_conn()
    with conn.cursor() as cursor:
        # conn.autocommit = True

        cursor.execute(
            f"select count(*) FROM mime_types_secondary where type_name = '{mime_name}';"
        )
        counter = cursor.fetchone()[0]
        if counter > 0:
            pass
        else:
            primary_mime_name = mime_name.split("/")[0]
            cursor.execute(
                f"select id FROM mime_types_primary where type_name = '{primary_mime_name}';"
            )
            primary_mime_id = cursor.fetchone()[0]
            cursor.execute(
                f"INSERT INTO mime_types_secondary (type_name, primary_mime_id) VALUES ('{mime_name}', {primary_mime_id});"
            )

        cursor.execute(
            f"""SELECT id as secondary_mime_id, primary_mime_id, 
            type_name, is_audio, is_video, html_video_ready, 
            html_audio_ready, search_enabled
            FROM mime_types_secondary where type_name = '{mime_name}';"""
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()][0]
    return data


def insertCategory():
    "category_name -> category_id"
    "нет в БД - создаем запись, есть в БД - возвращаем идентификаторы"
    return NotImplementedError


def insertType():
    "type_name -> type_id"
    "нет в БД - создаем запись, есть в БД - возвращаем идентификаторы"
    return NotImplementedError


def insertFile():
    "file -> file_hash"
    "нет в БД - создаем запись, есть в БД - возвращаем идентификаторы"
    return NotImplementedError


# получение данных из БД
def getBaseway(conn, test: bool = True):
    """
    Функция getBaseway возвращает базовый путь в библиотеке.
    Если параметр test равен True, функция выполняет запрос к базе данных с тестовым значением.
    Если параметр test равен False, функция выполняет запрос к базе данных с реальным значением.
    Если директория, указанная в результате запроса, существует, функция возвращает эту директорию.
    В противном случае функция вызывает исключение NotADirectoryError с сообщением 'Директория не найдена'.

    :param conn: соединение с базой данных
    :param test: флаг, указывающий на использование тестового значения (по умолчанию True)
    :return: базовый путь в библиотеке
    :raises NotADirectoryError: если директория, указанная в результате запроса, не существует
    """
    # conn = db_connection.get_conn()
    with conn.cursor() as cursor:
        cursor.execute(
            f"select parameter_value FROM config where parameter_name = 'filemanager.baseway' and test_value = '{test}';"
        )
        result = cursor.fetchone()[0]

    if os.path.exists(result) == True:
        return result
    else:
        raise NotADirectoryError("Директория не найдена")


def getCategoriesFromDB(conn, category_id=None):
    """
    Функция getCategoriesFromDB получает категории из базы данных и добавляет к каждой категории ее актуальный путь.
    Актуальный путь рассчитывается путем объединения базового пути библиотеки с путем категории.
    Если путь категории является абсолютным, он остается неизменным.
    Если в базе данных нет категорий, функция возвращает None.

    :param conn: соединение с базой данных
    :param category_id: идентификатор категории. Если None, то выбираются все категории.
    :return: список категорий с актуальными путями или None, если категорий нет в базе данных
    """
    baseway = getBaseway(conn)
    # conn = db_connection.get_conn()

    # select categories
    with conn.cursor() as cursor:
        addition = f"where id = {category_id}" if category_id != None else ""
        cursor.execute(
            f"select id as category_id, way, category_name, category_pseudonym, is_absolute_way from filestorage_categories {addition};"
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    # add actual way
    if len(data) > 0:
        for i in range(len(data)):
            full_way = (
                (baseway + data[i]["way"])
                if not data[i]["is_absolute_way"]
                else data[i]["way"]
            )
            data[i]["full_way"] = full_way
        return data
    else:
        return None


def getTypes(conn, category_id, type_id=None):
    """
    Функция getTypes получает типы из базы данных и добавляет к каждому типу его актуальный путь.
    Актуальный путь рассчитывается путем объединения базового пути библиотеки с путем типа.
    Если путь типа является абсолютным, он остается неизменным.
    Если в базе данных нет типов, функция возвращает None.

    :param conn: соединение с базой данных
    :param category_id: идентификатор категории.
    :return: список типов с актуальными путями или None, если типов нет в базе данных
    """
    # conn = db_connection.get_conn()

    # select categories
    with conn.cursor() as cursor:
        addition = f"and id = {type_id}" if type_id != None else ""
        cursor.execute(
            f"""select id as type_id, category_id, way, type_name, type_pseudonym, is_absolute_way 
            from filestorage_types where category_id = {category_id} {addition};"""
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    # add actual way
    if len(data) > 0:
        category_way = getCategoriesFromDB(conn, category_id=category_id)[0]['full_way']
        for i in range(len(data)):
            full_way = (
                (category_way + data[i]["way"])
                if not data[i]["is_absolute_way"]
                else data[i]["way"]
            )
            data[i]["full_way"] = full_way
        return data
    else:
        return None


def getFiles(conn, category_id, type_id, file_id = None):
    """
    Функция getFiles получает файлы из базы данных и добавляет к каждому файлу его полный путь.
    Полный путь рассчитывается путем объединения пути типа с путем файла.
    Если путь файла является абсолютным, он остается неизменным.
    Если в базе данных нет файлов, функция возвращает None.

    :param conn: соединение с базой данных
    :param category_id: идентификатор категории
    :param type_id: идентификатор типа
    :param file_id: идентификатор файла. Если None, то выбираются все файлы.
    :return: список файлов с полными путями или None, если файлов нет в базе данных
    """
    with conn.cursor() as cursor:
        addition = f"and id = {file_id}" if file_id != None else ""
        cursor.execute(
            f"""select id as file_id, type_id, way, filename, is_absolute_way, mime_type_id, size_kb
            from filestorage_files where type_id = {type_id} {addition};"""
        )
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    # add actual way
    if len(data) > 0:
        type_way = getTypes(conn, category_id=category_id, type_id=type_id)[0]['full_way']
        for i in range(len(data)):
            full_way = (
                (type_way + data[i]["way"] + data[i]["filename"])
                if not data[i]["is_absolute_way"]
                else data[i]["way"] + data[i]["filename"]
            )
            data[i]["full_way"] = full_way
        return data
    else:
        return None


# парсинг
def parseCategories(conn, reset=False):
    """
    Функция parseCategories проверяет наличие категорий в базе данных и обновляет их, если необходимо.
    Если параметр reset равен True, функция удаляет все категории из базы данных и добавляет их заново.
    Если параметр reset равен False, функция проверяет наличие категорий в базе данных и удаляет те, которые отсутствуют на диске.
    Функция возвращает список категорий после обновления.

    :param conn: соединение с базой данных
    :param reset: флаг, указывающий на необходимость полного обновления категорий (по умолчанию False)
    :return: список категорий после обновления
    """
    baseway = getBaseway(conn)
    # conn = db_connection.get_conn()

    # verify exist categories
    with conn.cursor() as cursor:
        # conn.autocommit = True
        if not reset:
            # get all categories from database
            cursor.execute(
                "select id as category_id, way, is_absolute_way from filestorage_categories;"
            )
            desc = cursor.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

            # verify non exist categories
            non_exist_categories = [
                f["category_id"]
                for f in data
                if not os.path.exists(
                    (baseway + f["way"]) if not f["is_absolute_way"] else f["way"]
                )
            ]

            # delete non exist categories from database
            if len(non_exist_categories) > 0:
                for c_id in non_exist_categories:
                    cursor.execute(
                        f"delete from filestorage_categories where id = {c_id};"
                    )
        else:
            cursor.execute("DELETE FROM filestorage_categories;")

        # add categories
        forbidden_first_symbols = ["_", "-", "."]
        conflict_addition = "ON CONFLICT (category_name) DO NOTHING"
        dirs = [
            f
            for f in os.listdir(baseway)
            if (os.path.isdir(baseway + f) or os.path.islink(baseway + f))
            and f[0] not in forbidden_first_symbols
        ]

        commands = [
            f"INSERT INTO filestorage_categories (category_name, way) VALUES ('{i}', '{i+'/'}') {conflict_addition};"
            for i in dirs
        ]
        for command in commands:
            cursor.execute(command)

    return getCategoriesFromDB(conn)


def parseTypes(conn, category_id, reset=False):
    """
    Функция parseTypes выполняет парсинг типов из базы данных и удаляет не существующие типы.

    :param conn: соединение с базой данных
    :param category_id: идентификатор категории.
    :param reset: Если True, то все типы и категории будут удалены из базы данных. По умолчанию False.

    :return: список типов категории после парсинга или None, если типов нет в базе данных
    """
    baseway = getBaseway(conn)
    # conn = db_connection.get_conn()

    with conn.cursor() as cursor:
        # conn.autocommit = True
        if not reset:
            for category in getCategoriesFromDB(conn, category_id=category_id):
                # get all types from database
                cursor.execute(
                    f"select id as type_id, category_id, way, is_absolute_way from filestorage_types where category_id = {category_id};"
                )
                desc = cursor.description
                column_names = [col[0] for col in desc]
                data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

                # verify exist types from database
                non_exist_types = [
                    f["type_id"]
                    for f in data
                    if not os.path.exists(
                        (baseway + category["way"] + f["way"])
                        if not f["is_absolute_way"]
                        else f["way"]
                    )
                ]

            if len(non_exist_types) > 0:
                for t_id in non_exist_types:
                    cursor.execute(f"delete from filestorage_types where id = {t_id};")
        else:
            cursor.execute(f"DELETE FROM filestorage_types where category_id = {category_id};")

        # add categories
        for category in getCategoriesFromDB(conn, category_id=category_id):
            category_id = category["category_id"]
            category_way = (
                baseway + category["way"]
                if not category["is_absolute_way"]
                else category["way"]
            )

            forbidden_first_symbols = ["_", "-", "."]
            conflict_addition = "ON CONFLICT (category_id, type_name) DO NOTHING"
            dirs = [
                f
                for f in os.listdir(category_way)
                if (os.path.isdir(category_way + f) or os.path.islink(category_way + f))
                and f[0] not in forbidden_first_symbols
            ]

            commands = [
                f"INSERT INTO filestorage_types (category_id, type_name, way) VALUES ({category_id}, $${i}$$, $${i+'/'}$$) {conflict_addition};"
                for i in dirs
            ]
            for command in commands:
                cursor.execute(command)

    return getTypes(conn, category_id)


def parseFiles(conn, category_id, type_id, reset=False):
    baseway = getBaseway(conn)
    # conn = db_connection.get_conn()

    with conn.cursor() as cursor:
        # conn.autocommit = True
        if not reset:
            for types in getTypes(conn, category_id=category_id, type_id=type_id):
                # get all types from database
                cursor.execute(
                    f"select id as file_id, type_id, way, filename, is_absolute_way from filestorage_files where type_id = {type_id};"
                )
                desc = cursor.description
                column_names = [col[0] for col in desc]
                data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

                # verify exist types from database
                non_exist_files = [
                    f["file_id"]
                    for f in data
                    if not os.path.exists(
                        (baseway + types["way"] + f["way"] + f["filename"])
                        if not f["is_absolute_way"]
                        else f["way"] + f["filename"]
                    )
                ]

            if len(non_exist_files) > 0:
                for f_id in non_exist_files:
                    cursor.execute(f"delete from filestorage_files where id = '{f_id}';")
        else:
            cursor.execute(f"DELETE FROM filestorage_files where type_id = {type_id};")

        # add categories
        for types in getTypes(conn, category_id=category_id, type_id=type_id):
            type_id = types["type_id"]
            type_way = types["full_way"][:-1]

            forbidden_first_symbols = ["_", "-", "."]
            with conn.cursor() as cursor:
                for root, dirs, files in os.walk(type_way):
                    data = []
                    root = root.replace("\\", "/")
                    way = root.replace(type_way, "") + '/'

                    for file in files:
                        if file[0] in forbidden_first_symbols:
                            continue
                        else:
                            full_way = f"{type_way + way + file}"
                            data.append(
                                {
                                    "way": way[1:],
                                    "filename": file,
                                    "type_id": type_id,
                                    "id": str(uuid.uuid4()),
                                    "mime_type_id": insertMIME(
                                        defineMIMEType(conn, full_way), conn
                                    )["secondary_mime_id"],
                                    "size_kb": int(os.path.getsize(full_way)/1024)
                                }
                            )
                    commands = [
                        "INSERT INTO filestorage_files (id, type_id, way, filename, mime_type_id, size_kb) "
                        f"VALUES ('{i['id']}', {type_id}, $${i['way']}$$, $${i['filename']}$$, {i['mime_type_id']}, {i['size_kb']});"
                        for i in data
                    ]

                    for command in commands:
                        cursor.execute(command)

    return getFiles(conn, category_id, type_id)


# Обновление Mime-типа для категории/типа
def updateMIMEonCategoriesTypes():
    return NotImplementedError


# работа с файлами
def renamer():
    return NotImplementedError



# worker
# conn = db_connection.get_conn()
# for category in parseCategories(conn):
#     result = parseTypes(conn, category_id=category["category_id"])
#     if result != None:
#         print(f'in {category['category_name']} (id: {category['category_id']}) found {len(result)} types')
#         for types in result:
#             files_result = parseFiles(conn, category_id=category["category_id"], type_id=types['type_id'])
#             if files_result != None:
#                 print(f'--- in {types['type_name']} (id: {types['type_id']}) found {len(files_result)} files')
#     else:
#         print(f'in {category['category_name']} (id: {category['category_id']}) 0 types')