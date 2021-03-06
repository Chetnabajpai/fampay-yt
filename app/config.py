from dotenv import find_dotenv, load_dotenv
from os import environ as env


app_env = env.get('APP_ENV')
if app_env:
    if app_env.upper() == 'TEST':
        env_file = '../test.env'
else:
    env_file = '.env'

# if env_file:
env_file = find_dotenv(env_file)
load_dotenv(env_file)

DATABASE_URL = env.get('DATABASE_URL')
REDIS_URL = env.get('REDIS_URL')
YOUTUBE_API_KEY = env.get('YOUTUBE_API_KEY')
YT_SEARCH_LINK = env.get('YT_SEARCH_LINK')
