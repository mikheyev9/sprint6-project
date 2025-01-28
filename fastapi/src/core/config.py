import os
from logging import config as logging_config
from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    project_name: str

    # Redis
    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str
    redis_db_index: int
    redis_dsn: str

    # Elasticsearch
    elasticsearch_dsn: str

    model_config = SettingsConfigDict(env_file='.env')



settings = Settings()
