from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager


from db.redis_cache import RedisCache
from api.routers import main_router
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление ресурсами FastAPI"""

    elastic_client = None

    try:
        redis_cache = RedisCache(settings)
        await redis_cache.connect()

        elastic_client = AsyncElasticsearch(hosts=[settings.elasticsearch_dsn])
        app.state.elastic = elastic_client

        yield

    finally:
    
        await redis_cache.close()

        if elastic_client:
            await elastic_client.close()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(main_router)
