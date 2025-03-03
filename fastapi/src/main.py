from contextlib import asynccontextmanager

from elasticsearch import AsyncElasticsearch
from fastapi.responses import ORJSONResponse
from src.api.routers import main_router
from src.core.config import elastic_settings, project_settings, redis_settings
from src.db.elastic_dao import ElasticDAO
from src.db.init_postgres import create_first_superuser
from src.db.redis_cache import RedisCacheManager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление ресурсами FastAPI."""

    elastic_client = None
    redis_cache_manager = RedisCacheManager(redis_settings)
    try:
        await create_first_superuser()
        await redis_cache_manager.setup()

        elastic_client = AsyncElasticsearch(hosts=[elastic_settings.dsn])
        app.state.elastic = ElasticDAO(elastic_client)

        yield

    finally:
        await redis_cache_manager.tear_down()

        if elastic_client:
            await elastic_client.close()


app = FastAPI(
    title=project_settings.project_name,
    docs_url="/openapi",
    openapi_url="/openapi.json",
    default_response_class=ORJSONResponse,
    summary=project_settings.project_summary,
    version=project_settings.project_version,
    terms_of_service=project_settings.project_terms_of_service,
    openapi_tags=project_settings.project_tags,
    lifespan=lifespan,
)

app.include_router(main_router)
