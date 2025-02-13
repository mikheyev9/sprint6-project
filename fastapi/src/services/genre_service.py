from http import HTTPStatus
from typing import List, Optional, Dict, Any
import logging

from fastapi import HTTPException

from db.abstract_db import AbstractDAO
from services.base_service import BaseService
from models.genre import GenresDTO, GenreDTO

logger = logging.getLogger(__name__)


class GenreService(BaseService[GenreDTO]):
    """Сервис для работы с жанрами в Elasticsearch."""

    service_name = "genre"

    def __init__(self, search_db: AbstractDAO):
        super().__init__(search_db, index="genres", model=GenreDTO)

    async def search(
        self,
        page_number: int = 1,
        page_size: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[GenreDTO]:
        """
        Возвращает список жанров из Elasticsearch с учётом пагинации и (опционально) фильтрации.
        """
        if filters is None:
            filters = {}

        # Для поиска с пагинацией используем offset/limit
        offset = (page_number - 1) * page_size

        response = await self.db.search(
            table=self.index,
            limit=page_size,
            offset=offset,
            filters=filters,
        )
        if not response:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='genres not found'
            )

        return [GenreDTO(**hit) for hit in response]