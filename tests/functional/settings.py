from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from .utils.logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class ServiceSettings(BaseSettings):
    """Настройки сервиса."""

    host: str
    port: int
    dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="SERVICE_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных."""

        self.dsn = f"http://{self.host}:{self.port}"


class ElasticsearchSettings(BaseSettings):
    """Настройки Elasticsearch."""

    host: str
    port: int
    dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="ELASTICSEARCH_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных."""

        self.dsn = f"http://{self.host}:{self.port}/"


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


service_settings = ServiceSettings()  # type: ignore
elasticsearch_settings = ElasticsearchSettings()  # type: ignore
redis_settings = RedisSettings()  # type: ignore
