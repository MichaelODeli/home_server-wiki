import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def getEnvValue(KEY):
    try:
        VALUE = os.environ.get(KEY)
        return VALUE
    except:
        return None