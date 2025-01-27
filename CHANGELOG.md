# Changelog

### [refactoring-2] - 12/10/2024
- Рефакторинг кода в соответствии с PEP8
  - Написание местозаполнителя для Docstrings

### [refactoring-1] - 18/09/2024
- Рефакторинг кода в соответствии с PEP8
  - Удаление неиспользуемых импортов (F401)
  - Форматирование импортов
  - Исправление сравнений с None (E711)
  - Исправление отступов и пробелов (W391, W293, E225, E302, E303)
  - Переименование функций в вид *lowercase_underscore*
  - Добавление заготовок текстов документации ко всем функциям в проекте

## ------ Этап `apps` ------
### [apps-10] - 17/09/2024
- Созданы заготовки новых приложений
- Разработка фронтэнда для приложения **Подписки**
- Разработка фронтэнда для приложения **Календарь**
- Исправления и улучшения
  - Исправлен цвет текста в светлой и темной теме
  - Генератор таблиц теперь использует Mantine компоненты
  - Добавлены новые ссылки в хедер
  - Перемещение страниц приложений в новые подпапки

### [apps-9] - 09/09/2024
- Добавлены оффлайн-копии CSS
    - Bootstrap
    - Шрифт Inter
- Добавлен [файл](./docs/project_info/APPS.md) для отслеживания готовности приложений
- Разработка макетов страниц для работы авторизации
    - В хедере добавлена кнопка выхода на специальные страницы
    - Страница авторизации (макет)
    - Страница личного кабинета (заготовка)
- Для главной страницы callback вынесены в отдельный модуль
- Обновление зависимостей
    - dash-2.17.1 -> dash-2.18.0
    - dash-extensions-1.0.17 -> dash-extensions-1.0.18

### [apps-8] - 03/09/2024
- Переход с Bootstrap компонентов на Mantine
    - Изменен основной цвет
    - Исправлены цвета у dmc.Progress и dmc.RingProgress
    - dbc.Button -> dmc.Button
    - html.H -> dmc.Title
    - Добавлена функция для создания кнопок Mantine со ссылками
- Разработка приложения **Аудиоплеер**
    - Получение перечня треков для выбранного плейлиста
    - Удаление неиспользуемых функций
- Прочие улучшения приложения
    - Фикс "прыгающего" dbc.Collapse в хедере
    - Добавление кнопок для открытия файла в результатах поиска

### [apps-7] - 01/09/2024
- Частичный переход на использование компонентов только из библиотеки Mantine
- Разработка приложения **Аудиоплеер**
    - Перемещение рендера элементов макета плейлиста в отдельную функцию
    - Добавлены заготовки страниц исполнителей, страниц альбомов, страницы поиска и главной страницы
    - Перемещение бокового меню в AppShellNavbar
    - Перемещение плеера в AppShellFooter

### [apps-6] - 31/08/2024
- Улучшение приложения **Видеоплеер**
    - Убрана тень у блоков
- Начало разработки **Аудиоплеера**
    - Убрана тень у блоков
    - Добавлено получение типов аудио из базы данных
    - Добавлена работа боковых кнопок выхода на плейлисты
    - Добавлена работа боковых кнопок выхода на главное меню
    - Создан макет плейлиста

### [apps-5] - 29/08/2024
- Улучшение хедера
    - Переписан dbc.Collapse 
    - Добавлено широкое поле поиска в основном приложении
    - Поле поиска в хедере скрывается на страницах поиска
- Исправлен порядок видео в результатах поиска видео
- Добавлен параметр с глубиной обхода файлового хранилища

### [apps-4] - 24/08/2024
- Улучшение приложения и виджета **Торренты**
    - Объединение контроллера для получения информации для виджета и для отдельной страницы
    - Добавлена ссылка для перехода на отдельную страницу qbittorrent
    - Добавление конфигурационных параметров в БД
    - Добавлен просмотр конфигурационных параметров в панели настроек

### [apps-3] - 23/08/2024
- Улучшение приложения **Видео**
    - Исправление высоты плеера
    - Фикс ложно срабатывающих callback на странице аудиоплеера
    - Добавлено отображение даты загрузки видео
    - Улучшение работы видеоплеера при попытке открыть несуществующий/невалидный видеофайл
    - Исправление расположения элементов видеоплеера
- Улучшение приложения **Торренты**
    - Добавлена работа чекбоксов для выбора нескольких торрентов
    - Начало разработки импортирования торрент-файлов для загрузки
    - Добавлена проверка magnet-ссылок на валидность
- Фиксы виджетов на главной странице
    - Отображение размеров активных разделов
    - Изменяемый цвет индикаторов в зависимости от нагрузки CPU/RAM/SWAP/дисков
- Исправлена работа переключателя светлой и темной темы

### [apps-2] - 21/08/2024
- Переименование проекта
- Исправление названий функций в соответствии с PEP8 (camelCase)
- Упрощение функции декодирования статуса торрента
- Исправление цвета текста в виджете на главной странице
- Получение ссылок для header из базы данных
- Улучшение приложения **Видео**
    - Работа главной страницы со случайными видео
    - Работа страницы поиска по видеороликам
    - Работа отображения похожих видео на странице просмотра
    - Исправление строки поиска
    - На миниатюре добавлено отображение длительности видео

### [apps-1] - 15/08/2024
- Переработка css-файлов
- Улучшения header приложения
    - Изменение структуры блока
    - Переписана форма поиска с *Purify с html* на html.Form
    - Улучшена кнопка переключения темы приложения
- Фикс отображения страниц на планшетах/смартфонах в горизонтальной ориентации
- Улучшение приложения **Видео**
    - Изменены ссылки на приложение
    - Главная страница со случайными видеороликами (макет)
    - Отдельный поисковик для видеороликов (макет)
    - Переработка стиля видеоплеера
    - Поиск в header ведется только по медиафайлам, доступным к просмотру на данной странице


## ------ Этап `server` ------
### [server-6] - 14/08/2024
- Завершение этапа **server**
- Блокировка приложения при отсутствии подключения к БД
- Подключение страниц приложения к новой базе данных
    - **Настройки**
        - Просмотр параметров из БД

### [server-5] - 12/08/2024
- Подключение страниц приложения к новой базе данных
    - **Видеоплеер**
        - Добавлены пустые файлы для новых разделов видеоплеера
        - ⚠️ Временно отключена кнопка загрузки видеофайла
    - **Поиск**
        - Полный переход на новый поисковый движок
        - Работа переключатей для форматирования ссылок на просмотр медиафайлов
        - Работа нового поиска в header приложения

### [server-4] - 12/08/2024
- Подключение страниц приложения к новой базе данных
    - **Поиск**
        - Постраничный просмотр результатов
        - Оформление результатов поиска
        - Адаптация страницы под мобильные устройства
        - Добавление параметров поиска для их будущей реализации

### [server-3] - 09/08/2024
- Подключение страниц приложения к новой базе данных
    - **Поиск** 
        - Просмотр имеющихся категорий и типов
        - Написание поисковых SQL-запросов под разные исходные данные
- В docker-compose добавлен httpd (как хост для прямого доступа к файлам)
    - ⚠️ Обратите внимание, что для конфигурации сервера используется файл httpd.conf со стандартными параметрами. Временно не рекомендуется использовать данный способ до фиксов.

### [server-2] - 08/08/2024
- Продолжение переработки парсера файлов
    - Добавление режимов парсинга
        - "*Обновление файлов*" - дополнение текущих категорий/типов новыми файлами
        - "*Обновление типов*" - добавление новых типов/файлов
        - "*Полное обновление*" - добавление новых категорий/типов/файлов
        - "*Сброс*" - удаление всех категорий/типов/файлов и сканирование "начисто"
    - Добавление информации о медиаконтенте в отдельную таблицу
    - Добавление механизма автоопределения основного mime-типа для категорий
        - Типы будут определяться только в режиме сброса. Вручную обновление можно будет запустить из ПУ.
    - В БД созданы view для быстрого просмотра списка файлов со всеми пояснениями
        - `filestorage_files_summary` - информация о всех файлах
        - `filestorage_mediafiles_summary` - информация о медиафайлах, дополненная соответствующей информацией
- Сокращение списка MIME-типов
    - Если нужен подробный список - [берем его тут](https://github.com/MichaelODeli/sql_mime_types)


### [server-1] - 07/08/2024
- Разработка новой структуры БД
- Размещение конфигурационных параметров в БД и в `.env` файле
- Добавление контроллера для подключения к БД
- Удален файл для первичной настройки сервера в связи с переходом к Docker
    - ⚠️ Проброс директорий для парсинга временно не настроен.
- **Начало переработки парсера файлов**
    - Адаптация для работы с PostgreSQL и с новой БД
    - Изменение логики работы
    - Файлы могут храниться в неограниченном количестве вложенных папок
- Исправление некоторых страниц
    - Видеоплеер: заготовка главной страницы
    - Поиск: исправление количества callback при вводе недостаточного количества символов
    - Настройки: изменен основной раздел на "О системе"


## ------ Этап `webui-rework` ------
### [webui-rework-1] - 01/08/2024
- Переход на новую систему версионирования
- Описание ближайших шагов разработки
- Переработка главной страницы
    - Добавление виджета мониторинга системы
    - Изменение виджета мониторинга объема дисков
- Дополнения страницы настроек
    - Добавление вкладки с характеристиками системы
    - Добавление вкладки с настройками виджетов и монитора торрентов


## ------ Этап `alpha` ------
### [alpha-3] - 28/06/2024
- Переход на dash-mantine-components 0.14.x
- Исправления dockerfile

### [alpha-2] - 21/04/2024
- Начата разработка [файла для подготовки БД и файлового хранилища к работе в приложении]()
- Начата разработка [README.md](README.md)

### [alpha-1] - 20/04/2024
- Начато использование changelog-а
- Переход на новую тему ZEPHYR
- Добавлен переключатель для темной темы
- Адаптация разделов приложения под новую тему оформления
- **Исправления домашней страницы**
    - html.Div -> dbc.Card
- **Исправления видеоплеера**
    - html.Div -> dbc.Card
    - Убран text-decoration у блока с рекомендуемыми видео
    - Увеличены некоторые отступы
    - Уменьшены кнопки разделов
- **Исправления аудиоплеера**
    - Фикс цветов кнопок
- **Исправления файлового менеджера**
    - Первый столбец имеет меньшую ширину (для флажков и значков)
    - dmc.Table -> dbc.Table