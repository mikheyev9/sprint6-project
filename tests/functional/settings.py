from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    # Elasticsearch
    elasticsearch_host: str
    elasticsearch_port: int
    elasticsearch_dsn: str

    # Redis
    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str
    redis_db_index: int
    redis_dsn: str

    # Fastapi
    service_host: str
    service_port: int
    service_dsn: str

    model_config = SettingsConfigDict(env_file='.env')


test_settings = TestSettings()
