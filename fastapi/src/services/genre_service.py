from http import HTTPStatus
from typing import List
import logging

from fastapi import HTTPException

from db.abstract_db import AbstractDAO
from services.base_service import BaseService
from models.genre import GenresDTO, GenreDTO

logger = logging.getLogger(__name__)


class GenreService(BaseService[GenresDTO]):
    """Сервис для работы с жанрами в Elasticsearch."""

    service_name = "genre"
    page_size = 50

    def __init__(self, search_db: AbstractDAO):
        super().__init__(search_db, index="genres", model=GenreDTO)

    async def search(self) -> List[GenreDTO]:
        """
        Возвращает список всех жанров из Elasticsearch.
        """
        response = await self.db.search(
            table=self.index,
            limit=self.page_size,
        )
        if not response:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='genres not found'
            )
        return [GenreDTO(**hit) for hit in response]
