from contextlib import asynccontextmanager

from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from src.api.routers import main_router
from src.core.config import jaeger_settings, project_settings, redis_settings
from src.core.jaeger import configure_tracer
from src.db.init_postgres import create_first_superuser
from src.db.redis_cache import RedisCacheManager
from src.db.postgres import create_database

from fastapi import FastAPI, Request, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление ресурсами FastAPI."""

    redis_cache_manager = RedisCacheManager(redis_settings)
    try:
        await create_database()
        await create_first_superuser()
        await redis_cache_manager.setup()

        yield

    finally:
        await redis_cache_manager.tear_down()


app = FastAPI(
    title=project_settings.project_auth_name,
    docs_url="/auth/openapi",
    openapi_url="/auth/openapi.json",
    default_response_class=ORJSONResponse,
    summary=project_settings.project_auth_summary,
    version=project_settings.project_auth_version,
    terms_of_service=project_settings.project_auth_terms_of_service,
    openapi_tags=project_settings.project_auth_tags,
    lifespan=lifespan,
)

app.include_router(main_router)

if jaeger_settings.debug:
    configure_tracer()
    FastAPIInstrumentor.instrument_app(app)


@app.middleware("http")
async def before_request(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "X-Request-Id is required"})
    return response
