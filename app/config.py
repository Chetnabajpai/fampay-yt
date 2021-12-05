from dotenv import find_dotenv, load_dotenv
from os import environ as env

env_file = None
app_env = env.get('APP_ENV')
if app_env:
    env_file = '.env'

if env_file:
    env_file = find_dotenv(env_file)
    load_dotenv(env_file)

DATABASE_URL = env.get('DATABASE_URL')
REDIS_URL = env.get('REDIS_URL')
YOUTUBE_API_KEY = env.get('YOUTUBE_API_KEY')
