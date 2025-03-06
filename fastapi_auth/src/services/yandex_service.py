from dataclasses import dataclass

import aiohttp
from fastapi.responses import RedirectResponse
from fastapi_users.exceptions import UserNotExists
from src.core.config import yandex_settings
from src.core.user_core import UserManager, auth_backend, get_user_manager
from src.schemas.user_schema import UserCreate

from fastapi import Depends


def get_yandex_service(user_manager: UserManager = Depends(get_user_manager)) -> "YandexService":
    """Функция для получения сервиса яндекса"""
    return YandexService(user_manager)


@dataclass
class YandexService:
    """Сервис для работы с Яндексом."""

    user_manager: UserManager

    async def get_yandex_code(self) -> str:
        """Получение данных для ссылки редиректа в Яндекс"""
        return RedirectResponse(yandex_settings.auth_url, status_code=307)

    async def get_yandex_token(self, code: str) -> str:
        """Получение на сайте Яндекса access_token"""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": yandex_settings.client_id,
            "client_secret": yandex_settings.client_secret,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(yandex_settings.token_url, data=data) as response:
                token_response = await response.json()
                return token_response.get("access_token")

    async def get_yandex_user_info(self, access_token: str) -> dict:
        """Получение данных на сайте Яндекса пользователя"""
        user_info_headers = {"Authorization": f"OAuth {access_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(yandex_settings.user_info_url, headers=user_info_headers) as response:
                return await response.json()

    async def login_yandex_user(self, code: str) -> dict:
        """Авторизация пользователя по данным Яндекса."""
        access_token = await self.get_yandex_token(code)
        user_info = await self.get_yandex_user_info(access_token)
        email = user_info["default_email"]
        try:
            user = await self.user_manager.get_by_email(email)
        except UserNotExists:
            password_hash = self.user_manager.password_helper.hash(email)
            user_data = UserCreate(
                email=email,
                password=password_hash,
                is_active=True,
                is_superuser=False,
                is_verified=True,
            )
            user = await self.user_manager.create(user_data)
        access_token = await auth_backend.get_strategy().write_token(user)
        return {"message": "Social login successful.", "email": email, "access_token": access_token}
