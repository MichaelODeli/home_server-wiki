# import logging
# logging.basicConfig(filename = "homeserver_worker.log", format = "%(asctime)s - %(levelname)s - %(message)s", level='INFO')

import glob
with open('fileManager.log', 'a', encoding='UTF-8') as file:
    file.write('\n----------\n\n')

import configparser
import os
import sqlite3
import sys
from datetime import datetime, date
import cv2 as cv
import traceback
import hashlib

videos_categories = ['cartoon_serials', 'en_serials', 'tv_shows', 'youtube', 'films', 'ru_serials']

def log_printer(task, data):
    """
    Вывод строки с датой и необходимой информацией
    """
    with open('fileManager.log', 'a', encoding='UTF-8') as file:
        now = datetime.now().strftime("%d/%b/%Y %H:%M:%S.%f")[:-3]
        string = f'fileManager - - [{now}] | {task} | {data}'
        print(string, file = file) # output to file
        print(string)

log_printer('main', 'app started')

def getCategoriesList(baseway: str):
    """
    Получение списка подпапок по заданной родительской папке.

    Параметры:
    - baseway - директория для поиска файлов. Строка должна кончаться на слэш/два обратных слэша
    """
    if baseway[-1] != '/' and baseway[-2:] != '\\\\':
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

def duration_with_opencv(filename):
    """
    Получение длительности видео с помощью OpenCV.

    -1 при невалидном видеофайле
    -2 при нулевом размере файла
    -3 при прочей ошибке
    """
    video = cv.VideoCapture(filename)
    if not video.isOpened(): 
        # need to catch errors
        duration = -1
    else:
        fps = video.get(cv.CAP_PROP_FPS)
        frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        duration = int(frame_count/fps)
    return duration

# получение текущей даты для БД
today = date.today()

# открытие конфиг-файла
try:
    cfg = configparser.ConfigParser()
    with open('new_settings.ini') as fp:
        cfg.read_file(fp)
except FileNotFoundError:
    raise FileNotFoundError("You didn't create config file (soon it will be automatic)")
log_printer('main', 'config read')
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
    if '-' in category or category[0]=='_': continue
    log_printer('main_loop', f'work with category "{category}"')
    basescript = f"""
                BEGIN TRANSACTION;
                DROP TABLE IF EXISTS "{category}";
                CREATE TABLE IF NOT EXISTS "{category}" (
                    '{category}_id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    '{category}_filehash' TEXT NOT NULL,
                    'type' TEXT NOT NULL,
                    'filename' TEXT UNIQUE NOT NULL,
                    'added' TEXT NOT NULL,
                    'size' INTEGER NOT NULL DEFAULT 0"""
    if category in videos_categories:
        basescript+=""",
                    'duration' INTEGER NOT NULL DEFAULT 0);"""
    else: basescript+=');'
    c.executescript(basescript) 
    conn.commit()
    log_printer('main_loop', 'table created')

    # # очистка базы от несуществующих файлов
    # c.execute(f'SELECT * FROM {category};')
    # linegroup = c.fetchall()
    # for line in linegroup:
    #     fullway = baseway+category+'/'+line[1]+'/'+line[2]
    #     if os.path.isfile(fullway) == False:
    #         c.execute(f'DELETE FROM {category} WHERE {category} = {line[0]}')
    # conn.commit()

    # добавление в базу новых файлов
    k=0
    data = getDataInCategory(baseway, category, data = 'files', addCategory=False)
    for fileListing in data:
        k+=1
        # получение типа и имени файла из его пути, а также формирование полного пути к файлу
        fileType = fileListing[0]
        fileName = fileListing[1]
        fullway = baseway+category+'/'+fileType+'/'+fileName
        log_printer('db_worker', f'{k}/{len(data)} | "{category}/{fileType}/{fileName}"')

        # получение хэша 
        calculated_hash = hashlib.sha1(bytes(fileName, encoding='UTF-8')).hexdigest()
        
        # получение размера файла
        fileSize = round(os.path.getsize(fullway)/1048576, 2)
        try:
            if category in videos_categories: 
                try:
                    fileDuration = duration_with_opencv(fullway) if fileSize > 0 else -2
                except Exception as e:
                    print(traceback.format_exc())
                    print(e)
                    fileDuration = -3
                c.execute(f'INSERT INTO {category} ({category}_filehash, type, filename, added, size, duration) VALUES ("{calculated_hash}", "{fileType}", "{fileName}", "{today}", "{fileSize}", "{fileDuration}");')
            else:
                c.execute(f'INSERT INTO {category} ({category}_filehash, type, filename, added, size) VALUES ("{calculated_hash}", "{fileType}", "{fileName}", "{today}", "{fileSize}");')
        except sqlite3.IntegrityError:
            pass
    
    # сброс последних значений id в таблице sqlite_sequence
    c.execute(f'UPDATE sqlite_sequence SET seq = (SELECT MAX({category}_id) FROM {category}) WHERE name="{category}"')
    conn.commit()
c.close()
conn.close()