from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager


from src.db.redis_cache import RedisCacheManager
from src.db.elastic_dao import ElasticDAO
from src.api.routers import main_router
from src.core.config import settings
from src.db.init_postgres import create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление ресурсами FastAPI."""
    
    elastic_client = None
    redis_cache_manager = RedisCacheManager(settings)
    try:
        await create_first_superuser()
        await redis_cache_manager.setup()

        elastic_client = AsyncElasticsearch(hosts=[settings.elasticsearch_dsn])
        app.state.elastic = ElasticDAO(elastic_client)

        yield

    finally:

        await redis_cache_manager.tear_down()

        if elastic_client:
            await elastic_client.close()


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    summary=settings.project_summary,
    version=settings.project_version,
    terms_of_service=settings.project_terms_of_service,
    openapi_tags=settings.project_tags,
    lifespan=lifespan,
)

app.include_router(main_router)
