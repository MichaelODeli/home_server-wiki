database_ip = '192.168.3.36' # manual setting
database_port = '5432' # manual setting
baseway = '' # manual setting

# settings for develop purpose
overwrite_existing_table = True # manual setting
all_categories = ['cartoon_serials', 'en_serials', 'tv_shows', 'youtube', 'films', 'ru_serials', 'apps', 'books', 'wiki'] 
videos_categories = ['cartoon_serials', 'en_serials', 'tv_shows', 'youtube', 'films', 'ru_serials']
search_avaliable_directories = 'ALL' # 'ALL" or list with inculded directories
create_directories = False
webui_ip = '0.0.0.0'
webui_port = 81

# settings table settings
settings_tablename = 'settings'
filemanager_tablename = 'filemanager'
filemanager_categories_tablename = 'filemanager_categories'
widgets_tablename = 'widgets'

# init database name
create_database_string = 'CREATE database home_server;'