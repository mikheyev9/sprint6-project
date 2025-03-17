from dataclasses import dataclass
from functools import lru_cache
from http import HTTPStatus
from typing import Any, Dict, List, Optional

from src.db.abstract_db import AbstractDAO
from src.db.elastic_dao import ElasticDAO, get_elastic
from src.models.genre import GenreDTO

from fastapi import Depends, HTTPException


@lru_cache()
def get_genre_service(
    db: ElasticDAO = Depends(get_elastic),
) -> "GenreService":
    return GenreService(db)


@dataclass
class GenreService:
    """Сервис для работы с жанрами."""

    db: AbstractDAO
    index: str = "genres"

    async def get_by_id(self, entity_id: str):
        """
        Получает жанр по ID.
        """

        doc = await self.db.get(table=self.index, id_obj=entity_id)

        if not doc:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{self.index} not found",
            )
        return GenreDTO(**doc)

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
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")

        return [GenreDTO(**hit) for hit in response]
