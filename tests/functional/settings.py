from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    # Elasticsearch
    elasticsearch_dsn: str
    elasticsearch_index: str

    # Redis
    redis_host: str
    redis_port: int

    # Fastapi
    service_url: str

    model_config = SettingsConfigDict(env_file='.env')


test_settings = TestSettings()
