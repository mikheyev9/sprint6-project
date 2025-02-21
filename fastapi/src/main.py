from contextlib import asynccontextmanager

from api.routers import main_router
from core.config import elastic_settings, project_settings, redis_settings
from db.elastic_dao import ElasticDAO
from db.redis_cache import RedisCacheManager
from elasticsearch import AsyncElasticsearch
from fastapi.responses import ORJSONResponse

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление ресурсами FastAPI"""

    elastic_client = None
    redis_cache_manager = RedisCacheManager(redis_settings)
    try:
        await redis_cache_manager.setup()

        elastic_client = AsyncElasticsearch(hosts=[elastic_settings.dsn])
        app.state.db = ElasticDAO(elastic_client)

        yield

    finally:
        await redis_cache_manager.tear_down()

        if elastic_client:
            await elastic_client.close()


app = FastAPI(
    title=project_settings.name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    summary=project_settings.summary,
    version=project_settings.version,
    terms_of_service=project_settings.terms_of_service,
    openapi_tags=project_settings.tags,
    lifespan=lifespan,
)

app.include_router(main_router)
