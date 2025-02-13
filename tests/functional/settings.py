from pydantic_settings import BaseSettings, SettingsConfigDict
from logging import config as logging_config

from .utils.logger import LOGGING_CONFIG
logging_config.dictConfig(LOGGING_CONFIG)


class TestSettings(BaseSettings):
    # Elasticsearch
    elasticsearch_host: str
    elasticsearch_port: int
    elasticsearch_dsn: str = ""

    # Redis
    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str
    redis_db_index: int
    redis_dsn: str = ""

    # FastAPI
    service_host: str
    service_port: int
    service_dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных"""
        
        self.elasticsearch_dsn = f"http://{self.elasticsearch_host}:{self.elasticsearch_port}/"
        self.redis_dsn = f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db_index}"
        self.service_dsn = f"http://{self.service_host}:{self.service_port}"


test_settings = TestSettings()
