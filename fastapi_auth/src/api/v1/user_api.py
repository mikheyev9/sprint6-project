from typing import List
from uuid import UUID

from src.core.config import project_settings
from src.core.user_core import (
    UserManager,
    auth_backend,
    current_superuser,
    current_user,
    fastapi_users,
    get_user_manager,
    refresh_auth_backend,
)
from src.db.redis_cache import RedisClientFactory
from src.models.user import User
from src.schemas.response_schema import ResponseSchema
from src.schemas.role_schema import RoleGetFull
from src.schemas.user_schema import UserCreate, UserRead, UserUpdate
from src.services.user_service import UserService, get_user_service

from fastapi import APIRouter, Depends, HTTPException, Request, status

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

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [route for route in users_router.routes if route.name != "users:delete_user"]
router.include_router(
    users_router,
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


@router.get("/{user_id}/roles", tags=["users"], summary="Get User Roles", response_model=List[RoleGetFull])
async def get_user_roles(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    user: User = Depends(current_superuser),
):
    """Список всех ролей установленный для пользователя. Доступно только для суперпользователей."""
    return await user_service.get_roles(user_id)


@router.post("/{user_id}/role", tags=["users"], summary="Add Role to User", response_model=ResponseSchema)
async def add_role_to_user(
    user_id: UUID,
    role_id: UUID,
    user_service: UserService = Depends(get_user_service),
    user: User = Depends(current_superuser),
) -> ResponseSchema:
    """Добавить роль пользователю. Доступно только для суперпользователей."""
    await user_service.add_role(user_id, role_id)
    return ResponseSchema(detail="Role added successfully")


@router.delete("/{user_id}/role", tags=["users"], summary="Remove Role from User", response_model=ResponseSchema)
async def remove_role_from_user(
    user_id: UUID,
    role_id: UUID,
    user_service: UserService = Depends(get_user_service),
    user: User = Depends(current_superuser),
) -> ResponseSchema:
    """Удалить роль у пользователя. Доступно только для суперпользователей."""
    await user_service.delete_role(user_id, role_id)
    return ResponseSchema(detail="Role removed successfully")
