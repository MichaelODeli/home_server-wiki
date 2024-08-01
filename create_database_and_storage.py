from config import *

# create table
def get_createtable_string(tablename):
    return f"""CREATE TABLE public.{tablename} (
    {tablename}_id SERIAL PRIMARY KEY,
    {tablename}_name varchar NOT NULL,
    {tablename}_value varchar NOT NULL
);
"""

# insert data
def get_insert_string(tablename, params_dict):
    params_list = tuple(params_dict.items())
    return f"""INSERT INTO {tablename} ({tablename}_name, {tablename}_value)
    VALUES
    {params_list};"""


# creating tables
get_createtable_string('settings_tablename')
get_createtable_string('filemanager_tablename')
get_createtable_string('filemanager_categories_tablename')
get_createtable_string('widgets_tablename')


# parameter_name - parameter_value
settings_dict = {
    "webui_ip": webui_ip,
    "webui_port": webui_port,
}
filemanager_dict = {
    "main_dir": baseway,
    "update_interval": '1',
}
widgets_dict = {
    'weather_city': 'Среднеуральск'
}

get_insert_string(settings_tablename, settings_dict)
get_insert_string(filemanager_tablename, filemanager_dict)

# columns

filemanager_categories_columns = {
    "category_id": "int",
    "category_name": "varchar",
    "category_isvideo": "bool",
    "category_scan_enable": "bool",
}
