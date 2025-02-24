from logging import config as logging_config
from pydantic import Field, EmailStr

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class ProjectSettings(BaseSettings):
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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="PROJECT_")


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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="POSTGRES_")

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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="ELASTICSEARCH_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных"""

        self.dsn = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class AuthSettings(BaseSettings):
    """Настройки авторизации."""

    secret: str = 'SECRET'
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
