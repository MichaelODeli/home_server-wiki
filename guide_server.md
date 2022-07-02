# Серверная оснастка

Структура файлов:
```
server-side/
    cgi-bin/
        search.py
        fileSorterGUI-server.py
        HTML.py.symlink
        settings.ini.symlink
        fileSearch.py.symlink
        fileManager.py.symlink
        storageLib_[type].ini.symlink
    storage/
        [type]/
            [category]/*.*
        settings.ini
        fileSearch.py
        fileManager.py
        storageLib_[type].ini
        mklinks.py
        HTML.py
    index.py
    videoview.py
```
> Обратите внимание, папка server-side должна быть прописана в конфигурации apache2 как домашняя директория (устанавливается при автоматической настройке).    
    
> Файлы с припиской `.symlink` относятся к своим оригиналам без данной приписки

---
## Раздел 1. Загрузка и установка необходимых зависимостей  
Чтобы избежать проблем с авторами устанавливаемого ПО, Вам необходимо установить его вручную. Настройка же производится автоматически после установки.
### Установка Webmin
[Официальный сайт](https://www.webmin.com/deb.html)
### Установка Transmission
Ubuntu:
```
sudo apt install transmission-daemon
```
### Установка Kiwix

---
## Раздел 2. Установка основного серверного ПО

---
## Раздел 3. Настройка основной серверной части

---
## Раздел 4. Управление серверной частью

---
## Раздел 5. Предустановленные модули и приложения

### webGUI
- Поиск по файлам в базе
- Воспроизведение видео из каталога (только mp4)
### Основная серверная оснастка
- Сортировка, обновление и перестроение файловой базы
- Поиск по файлам в базе
- Загрузка торрент-файлов (powered by Transmission)
- Просмотр Wiki (powered by Kiwix)
- Управление сервером (powered by Webmin)



