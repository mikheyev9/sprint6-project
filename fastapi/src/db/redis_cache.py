from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from core.config import Settings


class RedisCache:
    """Класс для управления подключением к Redis."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.redis_client: aioredis.Redis | None = None

    async def connect(self):
        if self.redis_client is None:
            self.redis_client = aioredis.from_url(self.settings.redis_dsn)
            FastAPICache.init(
                RedisBackend(self.redis_client),
                prefix="fastapi-cache"
            )

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()
