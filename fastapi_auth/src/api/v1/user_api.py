from typing import Annotated, Literal

from opentelemetry import trace
from opentelemetry.trace import SpanKind
from src.core.config import project_settings
from src.core.user_core import (
    UserManager,
    auth_backend,
    current_user,
    fastapi_users,
    get_user_manager,
    refresh_auth_backend,
)
from src.db.redis_cache import RedisClientFactory
from src.models.user import User
from src.schemas.user_schema import UserCreate, UserRead, UserUpdate
from src.services.auth_history_service import AuthHistoryService, get_auth_history
from src.services.vk_service import VkService, get_vk_service
from src.services.yandex_service import YandexService, get_yandex_service

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status

router = APIRouter()
tracer = trace.get_tracer(__name__)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)


@router.get(
    "/login-social/{social_name}",
    tags=["auth"],
    summary="Redirect to social",
    description="Redirect to social(Yandex, VK)",
)
async def login_social(
    request: Request,
    social_name: Annotated[
        Literal["yandex", "vk"],
        Path(
            title="Social_name service",
            description="Name of social service for redirect",
        ),
    ],
    vk_service: VkService = Depends(get_vk_service),
    yandex_service: YandexService = Depends(get_yandex_service),
):
    with tracer.start_as_current_span(
        "auth.login_social",
        kind=SpanKind.SERVER,
        attributes={"social_name": social_name, "http.request_id": request.headers.get("X-Request-Id")},
    ) as span:
        try:
            if social_name == "yandex":
                response = await yandex_service.get_yandex_code()
            elif social_name == "vk":
                response = await vk_service.get_vk_code()
            else:
                raise HTTPException(status_code=404, detail=f"Social provider:'{social_name}' not found")
            return response
        except Exception as e:
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            raise


@router.get(
    "/repass/yandex", tags=["auth"], summary="Callback yandex site", description="Callback yandex site with data"
)
async def auth_yandex(
    request: Request,
    code: Annotated[
        str,
        Query(
            title="Code for authorization",
            description="Code fore authorization",
        ),
    ],
    auth_service: AuthHistoryService = Depends(get_auth_history),
    service: YandexService = Depends(get_yandex_service),
):
    with tracer.start_as_current_span(
        "auth.callback.yandex",
        kind=SpanKind.SERVER,
        attributes={"http.request_id": request.headers.get("X-Request-Id")},
    ) as span:
        try:
            user_agent = request.headers.get("User-Agent")
            user, yandex_logined = await service.login_yandex_user(code)
            span.set_attribute("yandex_logined", True)
            await auth_service.create(user.id, user_agent)
            return yandex_logined
        except Exception as e:
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            raise


@router.get("/repass/vk", tags=["auth"], summary="Callback vk site", description="Callback vk site with data")
async def auth_vk(
    request: Request,
    code: Annotated[
        str,
        Query(
            title="Code for authorization",
            description="Code fore authorization",
        ),
    ],
    device_id: Annotated[
        str,
        Query(
            title="Device_id for authorization",
            description="Device_id fore authorization",
        ),
    ],
    state: Annotated[
        str,
        Query(
            title="State for authorization",
            description="State fore authorization",
        ),
    ],
    auth_service: AuthHistoryService = Depends(get_auth_history),
    service: VkService = Depends(get_vk_service),
):
    with tracer.start_as_current_span(
        "auth.callback.vk",
        kind=SpanKind.SERVER,
        attributes={"http.request_id": request.headers.get("X-Request-Id")},
    ) as span:
        try:
            user_agent = request.headers.get("User-Agent")
            user, vk_logined = await service.login_vk_user(code, device_id, state)
            await auth_service.create(user.id, user_agent)
            span.set_attribute("vk_logined", True)
            return vk_logined
        except Exception as e:
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            raise


users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [route for route in users_router.routes if route.name != "users:delete_user"]
router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/refresh",
    tags=["auth"],
    summary="Refresh Access Token",
    description="Refreshes the access token. Returns a new access token if successful.",
)
async def refresh_access_token(
    request: Request, user_manager: UserManager = Depends(get_user_manager), user: User = Depends(current_user)
):
    with tracer.start_as_current_span(
        "auth.refresh_token",
        kind=SpanKind.SERVER,
        attributes={"user_id": user.id if user else None, "http.request_id": request.headers.get("X-Request-Id")},
    ) as span:
        try:
            refresh_token = request.cookies.get("refresh_token")
            redis = await RedisClientFactory.create(project_settings.redis_dsn)
            payload = await refresh_auth_backend.get_strategy().read_token(refresh_token, user_manager)

            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Недействительный токен обновления",
                )

            stored_refresh_token = await redis.get(f"refresh_token:{payload.id}")

            if stored_refresh_token.decode("utf-8") != refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Недействительный токен обновления",
                )

            new_access_token = await auth_backend.get_strategy().write_token(payload)
            span.set_attribute("person_found", True)
            return {"access_token": new_access_token}
        except Exception as e:
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            raise
