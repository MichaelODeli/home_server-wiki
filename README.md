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

---
## О проекте.
Система управления серверной оснасткой со встроенными приложениями.   

---
## Структура проекта.
Проект представляет собой объединение некоторых репозиториев, для более удобного управления   
  
  
[Информационный репозиторий](https://github.com/MichaelODeli/home_server)   

### Клиент:
[localGUI-PC](https://github.com/MichaelODeli/home_server-localGUI) 
### Сервер:
[Библиотека 'File sorter'](https://github.com/MichaelODeli/home_server-filesorter)    
[webGUI]()
### Список доступных приложения для данных платформ   
[Список]()

---
## Установка и необходимые зависимости.
Для установки серверного и клиентского ПО используется автоустановщик с графическим интерфейсом (WIP)

[Инструкции и описние процесса установки на сервере]()  
[Инструкции и описние процесса установки на клиенте]()

---
## Запуск и работа проекта.
Серверное ПО запускается автоматически при загрузке системы, а также выполняет автоматическое обновление базы файлов по установленному времени.  
Клиентское ПО запускается пользователем. Оно автоматически проверяет обновления, а также необходимые файлы, загружаемые с сервера.

---
## Управление системами проекта.

### Панель для удаленного управления.
Apache2 with Python-cgi scripts
#### Доступные возможности:
- Поиск по файлам в базе
- Воспроизведение видео из каталога (только mp4)
- Платформа Webmin 1.994
- Kiwix (ПО для просмотра страниц Wikipedia)

### Панель для локального управления.
PySimpleGUI (TKinter)
#### Доступные возможности:
- Поиск по файлам в базе
- Воспроизведение видео из каталога (все форматы)
- Монитор системных показателей локального ПК
- Монитор системных показателей удаленного сервера