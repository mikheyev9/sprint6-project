import os
from logging import config as logging_config
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    project_name: str
    redis_host: str
    redis_port: int
    elastic_host: str
    elastic_port: int

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
