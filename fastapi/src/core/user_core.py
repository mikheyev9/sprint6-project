from datetime import datetime
from typing import Annotated, AsyncGenerator, Optional, Union
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    UUIDIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.db.postgres import get_async_session, get_session
from src.db.redis_cache import RedisClientFactory
from src.models.auth_history import AuthHistory
from src.models.user import User
from src.schemas.user_schema import UserCreate

from fastapi import Depends, Request

async def get_user_db(
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=auth_settings.secret, lifetime_seconds=auth_settings.jwt_lifetime_seconds)


def get_refresh_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=settings.jwt_refresh_lifetime_seconds)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

refresh_auth_backend = AuthenticationBackend(
    name="refresh_jwt",
    transport=bearer_transport,
    get_strategy=get_refresh_jwt_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    async def validate_password(self, password: str, user: Union[UserCreate, User]) -> None:
        if len(password) < settings.min_password_length:
            raise InvalidPasswordException(
                reason=f"Пароль должен содержать не менее {settings.min_password_length} символов")
        if user.email in password:
            raise InvalidPasswordException(reason="Пароль не может содержать ваш email")

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        print(f"Пользователь {user.email} зарегистрирован.")

    async def on_after_login(self, user: User, request: Request | None = None, response=None) -> None:
        redis = await RedisClientFactory.create(settings.redis_dsn)
        refresh_token = await refresh_auth_backend.get_strategy().write_token(user)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        session = await get_session()
        auth_entry = AuthHistory(
            user_id=user.id, user_agent=request.headers.get("User-Agent"), timestamp=datetime.now()
        )
        session.add(auth_entry)
        await session.commit()

        await redis.set(f"refresh_token:{user.id}", refresh_token)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend, refresh_auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
