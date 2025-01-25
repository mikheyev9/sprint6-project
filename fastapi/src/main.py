from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.db.redis_cache import setup_redis_cache
from api.routers import main_router
from core.config import settings
from db import elastic


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
        hosts=[f'{settings.elastic_host}:{settings.elastic_port}']
    )


@app.on_event('shutdown')
async def shutdown():
    await elastic.es.close()


app.include_router(main_router)
