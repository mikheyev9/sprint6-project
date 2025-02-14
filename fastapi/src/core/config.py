from logging import config as logging_config
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class Settings(BaseSettings):
    # FastAPI
    project_name: str
    project_summary: str
    project_version: str
    project_terms_of_service: str
    project_tags: list = Field(default=[
        {
            "name": 'films',
            "description": 'Operations with films.',
        },
        {
            "name": 'genres',
            "description": 'Operations with genres.',
        },
        {
            "name": 'persons',
            "description": 'Operations with persons.',
        },
    ])

    # Redis
    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str
    redis_db_index: int
    redis_dsn: str = ""

    # Elasticsearch
    elasticsearch_host: str
    elasticsearch_port: int
    elasticsearch_dsn: str = ""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных"""
        
        self.redis_dsn = f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db_index}"
        self.elasticsearch_dsn = f"http://{self.elasticsearch_host}:{self.elasticsearch_port}/"


settings = Settings()
