from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class BaseSettingsClass(BaseSettings):
    """Базовый класс для настроек."""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class ProjectSettings(BaseSettingsClass):
    """Настройки проекта."""

    name: str
    summary: str
    version: str
    terms_of_service: str
    tags: list = Field(
        default=[
            {
                "name": "films",
                "description": "Operations with films.",
            },
            {
                "name": "genres",
                "description": "Operations with genres.",
            },
            {
                "name": "persons",
                "description": "Operations with persons.",
            },
        ]
    )

    class Config:
        env_prefix = "PROJECT_"


class RedisSettings(BaseSettingsClass):
    """Настройки Redis."""

    host: str
    port: int
    user: str
    password: str
    db_index: int
    dsn: str = ""

    class Config:
        env_prefix = "REDIS_"


class ElasticSettings(BaseSettingsClass):
    """Настройки Elasticsearch."""

    host: str
    port: int
    dsn: str = ""

    class Config:
        env_prefix = "ELASTICSEARCH_"


project_settings = ProjectSettings()  # type: ignore
redis_settings = RedisSettings()  # type: ignore
elastic_settings = ElasticSettings()  # type: ignore
