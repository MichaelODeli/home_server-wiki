<!-- alt+m hotkey -->
# Документация по проекту 'Home server'
## Содержание
0. [Содержание](#содержание)
1. [О проекте.](#о-проекте)
1. [Структура проекта.](#структура-проекта)
1. [Установка и необходимые зависимости.](#установка-и-необходимые-зависимости)
1. [Запуск и работа проекта.](#запуск-и-работа-проекта)
1. [Управление системами проекта.](#управление-системами-проекта)
    - [Панель для удаленного управления.](#панель-для-удаленного-управления)
    - [Панель для локального управления.](#панель-для-локального-управления)
1. [Модуль 1. Загрузчик торрентов.](#модуль-1-загрузчик-торрентов)
1. [Модуль 2. Менеджер файлов.](#модуль-2-менеджер-файлов)
1. [Модуль 3. Менеджер подписок.](#модуль-3-менеджер-подписок)
1. [Модуль 4. Системный монитор.](#модуль-4-системный-монитор)
1. [Модуль 5. Сортировщик данных.](#модуль-5-сортировщик-данных)
1. [Модуль 6. Видеонаблюдение.](#модуль-6-видеонаблюдение)
1. [Модуль 7. Поиск.](#модуль-7-поиск)
1. [Модуль 8. Видеоплеер.](#модуль-8-видеоплеер)

## О проекте.
Система управления умным домом.   

## Структура проекта.
Проект представляет собой объединение некоторых репозиториев, для более удобного управления   
[Библиотека 'File sorter'](https://github.com/MichaelODeli/home_server-filesorter)   
[localGUI-PC](https://github.com/MichaelODeli/home_server-localGUI)   
[Информационный репозиторий](https://github.com/MichaelODeli/home_server)   

### Клиент:
[localGUI-PC](https://github.com/MichaelODeli/home_server-localGUI) может быть полноценно запущен с клиентского устройства с минимальным разрешением 1024*600. Включает все необходимые библиотеки   
Структура файлов:
```
localGUI-PC/
    localScreenGUI.py
    settings.ini
    fileSorterGUI-client.py
    storageLib_[type].ini #(загружается с сервера)
```
### Сервер:
Структура файлов:
```
server-side/
    cgi-bin/
        search.py
        systemstats.py
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
    index.html
    search.html
```
> Обратите внимание, папка server-side должна быть прописана в конфигурации apache2 как домашняя директория.    
    
> Файлы с припиской `.symlink` относятся к своим оригиналам без данной приписки
## Установка и необходимые зависимости.
WIP

## Запуск и работа проекта.
WIP

## Управление системами проекта.

### Панель для удаленного управления.
Apache2 with Python-cgi scripts
#### Доступные возможности:
- Поиск по файлам в базе
- Воспроизведение видео из каталога (только mp4)

### Панель для локального управления.
PySimpleGUI (TKinter)
#### Доступные возможности:
- Поиск по файлам в базе
- Воспроизведение видео из каталога (все форматы)
- Монитор системных показателей локального ПК

## Модуль 1. Загрузчик торрентов.
#### Статус
![Проблемы в реализации](https://img.shields.io/badge/status-Troubles%20in%20creating-red)
#### Используемые зависимости
`transmission`
<!-- #### Стуктура кода

#### Использование и возможности -->


## Модуль 2. Менеджер файлов.
#### Статус
![Работа в процессе](https://img.shields.io/badge/status-WIP-lightgrey)
#### Платформа для запуска
- localGUI-PC
- webGUI
#### Используемые зависимости
Встроенная библиотека `fileSorterGUI`
<!-- #### Стуктура кода -->
#### Использование и возможности
Вкладка 'Utils -> fileSorterGUI'

#### Использование и возможности
Библиотека запускается вручную с клиентского устройства. В процессе реализация в качеcтве веб-приложения.

## Модуль 3. Менеджер подписок.
#### Статус
![Работа в процессе](https://img.shields.io/badge/status-WIP-lightgrey)
#### Платформа для запуска
- localGUI-PC
- webGUI
#### Используемые зависимости
Встроенная библиотека `subsManager`
<!-- #### Стуктура кода -->
#### Использование и возможности
Вкладка 'Subs' (localGUI-PC)

## Модуль 4. Системный монитор.
#### Статус
![Работа в процессе](https://img.shields.io/badge/status-WIP-lightgrey)
#### Платформа для запуска
- localGUI-PC
#### Используемые зависимости
Сторонняя библиотека `psutil`
#### Стуктура кода
По нажатию пользователем кнопки 'Update stats', происходит обновление системных показателей **клиента** - потребление ОЗУ и процент нагрузки ЦП.
#### Использование и возможности
Вкладка 'Stats'

## Модуль 5. Сортировщик данных.
#### Статус
![Released](https://img.shields.io/badge/status-released-green)
#### Платформа для запуска
- Только на серверной стороне по расписанию
#### Используемые зависимости
Встроенная библиотека `fileManager`
<!-- #### Стуктура кода -->
#### Использование и возможности
По расписанию из crontab

## Модуль 6. Видеонаблюдение.
#### Статус
![Работа в процессе](https://img.shields.io/badge/status-WIP-lightgrey)
#### Платформа для запуска
- localGUI-PC
<!-- #### Используемые зависимости -->
<!-- #### Стуктура кода -->
<!-- #### Использование и возможности -->

## Модуль 7. Поиск.
#### Статус
![Released](https://img.shields.io/badge/status-released-green)
#### Платформа для запуска
- localGUI-PC
- webGUI
#### Используемые зависимости
Встроенная библиотека `fileSearch`
<!-- #### Стуктура кода -->
#### Использование и возможности
Вкладка 'Search' (localGUI-PC) или панель поиска (webGUI)

## Модуль 8. Видеоплеер.
#### Статус
![Released](https://img.shields.io/badge/status-released-green)
#### Платформа для запуска
- localGUI-PC
- webGUI (только *.mp4)
#### Используемые зависимости
`vlc`
<!-- #### Стуктура кода -->
#### Использование и возможности
Вкладка 'Video' (localGUI-PC) или из поиска (webGUI)
