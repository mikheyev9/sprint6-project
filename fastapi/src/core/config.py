import os
from logging import config as logging_config
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    project_name: str
    redis_host: str
    redis_port: int
    elasticsearch_dsn: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
