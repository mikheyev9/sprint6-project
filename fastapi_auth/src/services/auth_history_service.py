from dataclasses import dataclass
from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUDBase
from src.db.postgres import get_async_session
from src.models.auth_history import AuthHistory
from src.schemas.auth_shema import AuthGetHistory, AuthCreateHistory


def get_auth_history(session: AsyncSession = Depends(get_async_session)) -> "AuthHistoryService":
    """Функция для получения истории входов."""
    return AuthHistoryService(session)


@dataclass
class AuthHistoryService:
    session: AsyncSession
    auth: CRUDBase = CRUDBase(AuthHistory)

    async def get_history(self, obj_id: UUID, limit: int = None) -> List[AuthGetHistory]:
        """Получение своей истории входа в аккаунт"""
        auth_histories = await self.session.execute(
            self.auth.get_query()
            .where(self.auth.model.user_id == obj_id)
            .limit(limit if limit else None)
        )
        return [
            AuthGetHistory.model_validate(auth_history)
            for auth_history in auth_histories.scalars().all()
        ]

    async def create(self, data: AuthCreateHistory) -> AuthGetHistory:
        """Создание записи при входе пользователя в аккаунт"""
        auth_history = await self.auth.create(data, self.session)
        return AuthGetHistory.model_validate(auth_history)
