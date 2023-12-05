import logging
logging.basicConfig(filename = "homeserver_worker.log", format = "%(asctime)s - %(levelname)s - %(message)s", level='INFO')
try:
    import glob
    import configparser
    import os
    import sqlite3
    import sys
    from datetime import date
    from moviepy.editor import VideoFileClip
except ImportError as e:
    logging.error('ImportError '+e)
    raise e

today = date.today()

cfg = configparser.ConfigParser()
with open('new_settings.ini') as fp:
    cfg.read_file(fp)

# конфиг
if sys.platform == "linux" or sys.platform == "linux2":
    baseway = cfg.get('settings', 'LinWay')
elif sys.platform == "win32":
    baseway = cfg.get('settings', 'WinWay')
# baseway = '/mnt/c/Users/MichaelODeli/OneDrive/DEVELOP/work/home-server/updated_server-side/storage/'

baseName = 'storage.sqlite3'
DBway = baseway+baseName

# функция для получения списка категорий по названиям папок. служебные папки начинаются с нижнего подчеркивания
def getCategoriesList(baseway):
    categoriesList = glob.glob(baseway+'**/', recursive=False)
    newlist = []
    for element in categoriesList:
        cleared = element.replace('\\', '/').replace(baseway, '').replace('/', '')
        if cleared[0] == '_': 
            pass
        else:
            newlist.append(cleared)
    return(newlist)

def getDataInCategory(baseway, category, data, addCategory=True):
    if data == 'files': param = '/*/*.*'
    if data == 'types': param = '/**/'
    dataList = glob.glob(baseway+category+param, recursive=True)
    for i in range(len(dataList)):
        dataList[i] = dataList[i].replace('\\', '/').replace(baseway, '').split('/')
        if data == 'types': del dataList[i][-1]  # because last symbol '/' create empty list element
        if addCategory == False: del dataList[i][0]
    if data == 'types': del dataList[0]  # libname
    return(dataList)

def filesRenamer(baseway):
    fileList = glob.glob(baseway+'/*/*/*.*', recursive=True)
    for i in range(len(fileList)):
        fileList[i] = fileList[i].replace('\\', '/')
    for element in fileList:
        fileSplit = element.split('/')
        restricted = ['#', '$', '%', '+', '*', '&', '?', '=']
        for j in restricted:
            fileSplit[-1] = fileSplit[-1].replace(j, '')
        fileSplit[-1] = fileSplit[-1].replace('  ', ' ').replace('   ', ' ').replace('__', '_').replace('___', '_').replace('--', '-').replace('---', '-')
        fileSplit='/'.join(fileSplit)
        os.rename(element, fileSplit)

filesRenamer(baseway)

conn = sqlite3.connect(baseName)
c = conn.cursor()
for category in getCategoriesList(baseway):
    basescript = f"""
                BEGIN TRANSACTION;
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

    # очистка базы от несуществующих файлов
    c.execute('SELECT * FROM {categ};'.format(categ=category))
    linegroup = c.fetchall()
    for line in linegroup:
        fullway = baseway+category+'/'+line[1]+'/'+line[2]
        if os.path.isfile(fullway) == False:
            c.execute(f'DELETE FROM {category} WHERE {category} = {line[0]}')
    conn.commit()

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
                c.execute(f'INSERT OR IGNORE INTO {category} (type, filename, added, size, duration) VALUES ("{fileType}", "{fileName}", "{today}", "{fileSize}", "{fileDuration}");')
            else:
                c.execute(f'INSERT OR IGNORE INTO {category} (type, filename, added, size) VALUES ("{fileType}", "{fileName}", "{today}", "{fileSize}");')
        except sqlite3.IntegrityError:
            pass
    
    # сброс последних значений id в таблице sqlite_sequence
    c.execute(f'UPDATE sqlite_sequence SET seq = (SELECT MAX({category}) FROM {category}) WHERE name="{category}"')
    conn.commit()
c.close()
conn.close()