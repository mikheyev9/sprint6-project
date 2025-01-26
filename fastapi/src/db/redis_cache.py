from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.core.config import Settings


async def setup_redis_cache(settings: Settings) -> None:
    """
    Настраивает кеширование через FastAPICache с использованием Redis.
    """
    redis_connection = aioredis.from_url(settings.redis_dsn)
    FastAPICache.init(RedisBackend(redis_connection), prefix="fastapi-cache")
