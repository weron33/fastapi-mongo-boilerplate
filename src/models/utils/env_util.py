import os

from dotenv import load_dotenv


def set_env():
    if os.environ['API_ENV'] == 'development':
        load_dotenv("src/envs/dev-env/.env")
    elif os.environ['API_ENV'] == 'docker':
        load_dotenv("src/envs/docker-env/.env")
    else:
        load_dotenv("src/envs/prod-env/.env")
