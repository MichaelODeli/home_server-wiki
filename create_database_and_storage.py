database_ip = ''
database_port = ''
baseway = ''
overwrite_existing_table = True
videos_categories = ['cartoon_serials', 'en_serials', 'tv_shows', 'youtube', 'films', 'ru_serials']
other_categories = ['apps', 'books', 'wiki']
search_avaliable_directories = 'ALL' # 'ALL" or list with inculded directories
create_directories = False
webui_ip = ''
webui_port = ''


settings_tablename = 'settings'
setting_id_columname = 'setting_id'
setting_name_columname = 'setting_name'
setting_value_columname = 'setting_value'

create_database_string = 'CREATE database home_server'

create_table_string = f'''CREATE TABLE public.{settings_tablename} (
	{setting_id_columname} varchar NOT NULL,
	{setting_name_columname} varchar NOT NULL,
	{setting_value_columname} varchar NOT NULL,
	CONSTRAINT {settings_tablename}_pk PRIMARY KEY ({setting_id_columname})
);
'''

settings_dict = {
    'database_ip': database_ip,
    'database_port' : database_port,
    'filemanager_baseway': baseway,
    'videos_categories': str(videos_categories).replace("'", "").replace(" ", "")[1:-1],
    'other_categories': str(other_categories).replace("'", "").replace(" ", "")[1:-1],
    'webui_ip': webui_ip,
    'webui_port': webui_port
}

print(settings_dict)