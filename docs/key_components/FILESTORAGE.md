# Структура файлового хранилища
В приложении принята следующая структура файлового хранилища
```
baseway/
├── category/
│   ├── filetype/
│   │   └── filename.mp4
│   └── filetype/
│       └── filename.csv
└── category/
    ├── filetype/
    │   └── filename.mp3
    └── filetype/
        └── filename.html
```
- **baseway** - основной путь, в котором будет находиться библиотека файлов
- **category** - категория файлов (apps/videos/photos)
- **filetype** - подкатегория файла (вид приложения/год съемки видео/место снятия фотографий)
- **filename** - название файлов