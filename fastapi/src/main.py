from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from src.api.routers import main_router
from src.core.config import settings
from src.db import elastic
from src.db import redis


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    await setup_redis_cache(settings)
    elastic.es = AsyncElasticsearch(
        hosts=[f'{settings.elasticsearch_dsn}']
    )


@app.on_event('shutdown')
async def shutdown():
    await elastic.es.close()


app.include_router(main_router)
