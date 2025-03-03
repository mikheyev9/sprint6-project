from logging import config as logging_config
from typing import Optional


from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class ProjectSettings(BaseSettings):
    # FastAPI
    project_name: str
    project_summary: str
    project_version: str
    project_terms_of_service: str
    project_tags: list = Field(
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

    # Postgres
    postgres_db_name: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_dsn: str = ""

    # Auth
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    jwt_lifetime_seconds: int = 3600
    jwt_refresh_lifetime_seconds: int = 86400
    min_password_length: int = 3

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    debug: bool = False

class RedisSettings(BaseSettings):
    """Настройки Redis."""

    host: str
    port: int
    user: str
    password: str
    db_index: int
    dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="REDIS_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных."""

        self.dsn = f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_index}"


class ElasticSettings(BaseSettings):
    """Настройки Elasticsearch."""

    host: str
    port: int
    dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="ELASTICSEARCH_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных."""

        self.dsn = f"http://{self.host}:{self.port}/"


class PostgresSettings(BaseSettings):
    """Настройки Postgres."""

    db_name: str
    host: str
    port: int
    user: str
    password: str
    dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="POSTGRES_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных"""

        self.dsn = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class AuthSettings(BaseSettings):
    """Настройки авторизации."""

    secret: str = "SECRET"
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None
    jwt_lifetime_seconds: int = 3600
    min_password_lenght: int = 3

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


project_settings = ProjectSettings()  # type: ignore
redis_settings = RedisSettings()  # type: ignore
elastic_settings = ElasticSettings()  # type: ignore
postgres_settings = PostgresSettings()  # type: ignore
auth_settings = AuthSettings()  # type: ignore
