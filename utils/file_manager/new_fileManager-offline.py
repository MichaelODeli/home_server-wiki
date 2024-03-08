# import logging
# logging.basicConfig(filename = "homeserver_worker.log", format = "%(asctime)s - %(levelname)s - %(message)s", level='INFO')

import glob
import configparser
import os
import sqlite3
import sys
from datetime import datetime
from datetime import date
from moviepy.editor import VideoFileClip

def log_printer(task, data):
    """
    Вывод строки с датой и необходимой информацией
    """
    now = datetime.now().strftime("%d/%b/%Y %H:%M:%S") 
    print(
        f'fileManager - - [{now}] | {task} | {data}'
    )

def getCategoriesList(baseway: str):
    """
    Получение списка подпапок по заданной родительской папке.

    Параметры:
    - baseway - директория для поиска файлов. Строка должна кончаться на слэш/два обратных слэша
    """
    if baseway[-1] != '/' and baseway[-2:] != '//':
        raise ValueError('In the end of baseway string you must provide "/" or "\\\\" symbols.')
    dirs_list = [f.path.replace(baseway, '') for f in os.scandir(baseway) if f.is_dir()]
    if len(dirs_list) == 0: 
        raise FileExistsError("Parent's folder exists, but child folders isn't found.")
    else:
        dirs = [x for x in dirs_list if x[0] != '_']
        log_printer('getCategoriesList', f"found this categories: {', '.join(dirs)}")
        return dirs

def getDataInCategory(baseway, category, data, addCategory=True):
    "Legacy. Will be rewrited."
    if data == 'files': 
        param = '/*/*.*'
    if data == 'types': 
        param = '/**/'
    dataList = glob.glob(baseway+category+param, recursive=True)
    for i in range(len(dataList)):
        dataList[i] = dataList[i].replace('\\', '/').replace(baseway, '').split('/')
        if data == 'types': 
            del dataList[i][-1]  # because last symbol '/' create empty list element
        if addCategory == False: 
            del dataList[i][0]
    if data == 'types': 
        del dataList[0]  # libname
    return dataList

def filesRenamer(baseway):
    "Legacy. Will be rewrited."
    log_printer('filesRenamer', 'started')

    fileList = glob.glob(baseway+'/*/*/*.*', recursive=True)
    log_printer('filesRenamer', f'total files: {len(fileList)}')
    for i in range(len(fileList)):
        fileList[i] = fileList[i].replace('\\', '/')
    for element in fileList:
        # надо подумать, стоит ли отдельно проверять 
        fileSplit = element.split('/')
        restricted = ['#', '$', '%', '+', '*', '&', '?', '=']
        for j in restricted:
            fileSplit[-1] = fileSplit[-1].replace(j, '')
        fileSplit[-1] = fileSplit[-1].replace('  ', ' ').replace('   ', ' ').replace('__', '_').replace('___', '_').replace('--', '-').replace('---', '-')
        fileSplit='/'.join(fileSplit)
        k = 0
        if element != fileSplit: 
            k +=1
            os.rename(element, fileSplit)
    log_printer('filesRenamer', f'renamed files: {k}')

# получение текущей даты для БД
today = date.today()

# открытие конфиг-файла
try:
    cfg = configparser.ConfigParser()
    with open('new_settings.ini') as fp:
        cfg.read_file(fp)
except FileNotFoundError:
    raise FileNotFoundError("You didn't created config file (soon it will be automatic)")

# конфиг
if sys.platform == "linux" or sys.platform == "linux2":
    baseway = cfg.get('settings', 'LinWay')
elif sys.platform == "win32":
    baseway = cfg.get('settings', 'WinWay')

baseName = 'storage.sqlite3'
DBway = baseway+baseName

filesRenamer(baseway)

conn = sqlite3.connect(baseName)
c = conn.cursor()
for category in getCategoriesList(baseway):
    log_printer('main_loop', f'work with category "{category}"')
    basescript = f"""
                BEGIN TRANSACTION;
                DROP TABLE IF EXISTS "{category}";
                CREATE TABLE IF NOT EXISTS "{category}" (
                    '{category}' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'type' TEXT NOT NULL,
                    'filename' TEXT UNIQUE NOT NULL,
                    'added' TEXT NOT NULL,
                    'size' INTEGER NOT NULL DEFAULT 0"""
    if category == 'youtube' or category == 'films':
        basescript+=""",
                    'duration' INTEGER NOT NULL DEFAULT 0);"""
    else: basescript+=');'
    c.executescript(basescript) 
    conn.commit()

    # # очистка базы от несуществующих файлов
    # c.execute(f'SELECT * FROM {category};')
    # linegroup = c.fetchall()
    # for line in linegroup:
    #     fullway = baseway+category+'/'+line[1]+'/'+line[2]
    #     if os.path.isfile(fullway) == False:
    #         c.execute(f'DELETE FROM {category} WHERE {category} = {line[0]}')
    # conn.commit()

    # добавление в базу новых файлов
    for fileListing in getDataInCategory(baseway, category, data = 'files', addCategory=False):
        fileType = fileListing[0]
        fileName = fileListing[1]
        fullway = baseway+category+'/'+fileType+'/'+fileName
        fileSize = os.path.getsize(fullway)
        try:
            fileSize = round(os.path.getsize(fullway)/1048576, 2)
            if category == 'youtube' or category == 'films': 
                try:
                    fileDuration = VideoFileClip(fullway).duration
                except OSError:
                    fileDuration = -1
                c.execute(f'INSERT INTO {category} (type, filename, added, size, duration) VALUES ("{fileType}", "{fileName}", "{today}", "{fileSize}", "{fileDuration}");')
            else:
                c.execute(f'INSERT INTO {category} (type, filename, added, size) VALUES ("{fileType}", "{fileName}", "{today}", "{fileSize}");')
        except sqlite3.IntegrityError:
            pass
    
    # сброс последних значений id в таблице sqlite_sequence
    c.execute(f'UPDATE sqlite_sequence SET seq = (SELECT MAX({category}) FROM {category}) WHERE name="{category}"')
    conn.commit()
c.close()
conn.close()