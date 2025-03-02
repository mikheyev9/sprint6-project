from fastapi import APIRouter, Depends, Request, HTTPException, status
from src.core.user_core import UserManager, auth_backend, refresh_auth_backend, fastapi_users, get_user_manager
from src.schemas.user_schema import UserCreate, UserRead, UserUpdate
from src.core.config import settings
from src.db.redis_cache import RedisClientFactory
from src.depends.get_user_data import get_refresh_data

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes if route.name != 'users:delete_user'
]
router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)

@router.post("/auth/refresh", tags=["auth"])
async def refresh_access_token(
    request: Request,
    user_manager: UserManager = Depends(get_user_manager)
):
    refresh_token = request.cookies.get('refresh_token')
    redis = await RedisClientFactory.create(settings.redis_dsn)
    payload = await refresh_auth_backend.get_strategy().read_token(refresh_token, user_manager)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен обновления",
        )

    stored_refresh_token = await redis.get(f"refresh_token:{payload.id}")

    if stored_refresh_token.decode('utf-8') != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен обновления",
        )

    new_access_token = await auth_backend.get_strategy().write_token(payload)

    return {"access_token": new_access_token}

