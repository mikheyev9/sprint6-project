from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    # Elasticsearch
    elasticsearch_dsn: str
    elasticsearch_index: str

    # Redis
    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str
    redis_db_index: int
    redis_dsn: str

    # Fastapi
    service_url: str

    model_config = SettingsConfigDict(env_file='.env')


test_settings = TestSettings()
