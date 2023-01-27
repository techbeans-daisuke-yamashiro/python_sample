from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")
PROJECT_NAME = "FastAPI Sample"
VERSION = "0.0.0"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")
ACCESS_TOKEN_EXPIRES_IN=config("ACCESS_TOKEN_EXPIRES_IN",cast=int,default=60)
REFRESH_TOKEN_EXPIRES_IN=config("REFRESH_TOKEN_EXPIRES_IN",cast=int,default=60)

DB_USER = config("DB_USER", cast=str)
DB_PASSWORD = config("DB_PASSWORD", cast=Secret)
DB_SERVER = config("DB_SERVER", cast=str, default="localhost")
DB_PORT = config("DB_PORT", cast=str, default="5432")
DB_NAME = config("DB_NAME", cast=str)
DB_ENGINE = config("DB_ENGINE", cast=str)
DB_ECHO = config("DB_ECHO",cast=bool,default=False)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=str,
    default=f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/'
        f'{DB_NAME}')