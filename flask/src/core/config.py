from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class ProjectSettings(BaseSettings):
    """Данные проекта"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


project_settings = ProjectSettings()  # type: ignore
