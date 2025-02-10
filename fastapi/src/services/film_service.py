import logging
from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from db.abstract_db import AbstractDAO
from services.base_service import BaseService
from models.film import MovieInfoDTO, MovieBaseDTO

logger = logging.getLogger(__name__)


class FilmService(BaseService[MovieInfoDTO]):
    service_name = 'film'

    def __init__(self, search_db: AbstractDAO):
        super().__init__(search_db, index="movies", model=MovieInfoDTO)

    async def search(
        self,
        genre: str | None = None,
        page_size: int = 50,
        page_number: int = 1,
        sort: str = "imdb_rating",
        title: str | None = None
    ) -> List[MovieBaseDTO]:
        """
        Получает список фильмов из Elasticsearch
        с поддержкой фильтрации, сортировки и пагинации.
        """
        filters = {}
        if genre:
            filters["genre.name"] = genre
        if title:
            filters["title"] = title
        response = await self.db.search(
            table=self.index,
            offset=(page_number - 1) * page_size,
            limit=page_size,
            sort=[{sort: "desc"}],
            filters=filters,
        )
        if not response:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='films not found'
            )
        return [MovieBaseDTO(**hit) for hit in response]
