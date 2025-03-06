from typing import Annotated, Literal

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
from src.services.vk_service import VkService, get_vk_service
from src.services.yandex_service import YandexService, get_yandex_service

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status

router = APIRouter()

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
    if social_name == "yandex":
        return await yandex_service.get_yandex_code()
    elif social_name == "vk":
        return await vk_service.get_vk_code()
    else:
        raise HTTPException(status_code=404, detail=f"Social provider:'{social_name}' not found")


@router.get(
    "/repass/yandex", tags=["auth"], summary="Callback yandex site", description="Callback yandex site with data"
)
async def auth_yandex(
    code: Annotated[
        str,
        Query(
            title="Code for authorization",
            description="Code fore authorization",
        ),
    ],
    service: YandexService = Depends(get_yandex_service),
):
    return await service.login_yandex_user(code)


@router.get("/repass/vk", tags=["auth"], summary="Callback vk site", description="Callback vk site with data")
async def auth_vk(
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
    service: VkService = Depends(get_vk_service),
):
    return await service.login_vk_user(code, device_id, state)


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

    return {"access_token": new_access_token}
