from dataclasses import dataclass
from functools import lru_cache
from http import HTTPStatus
from typing import List

from src.db.abstract_db import AbstractDAO
from src.db.elastic_dao import ElasticDAO, get_elastic
from src.models.film import MovieBaseDTO, MovieInfoDTO

from fastapi import Depends, HTTPException


@lru_cache()
def get_film_service(
    db: ElasticDAO = Depends(get_elastic),
) -> "FilmService":
    return FilmService(db)


@dataclass
class FilmService:
    """Сервис для работы с фильмами."""

    db: AbstractDAO
    index: str = "movies"

    async def get_by_id(self, entity_id: str):
        """
        Получает объект по ID.
        """

        doc = await self.db.get(table=self.index, id_obj=entity_id)

        if not doc:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{self.index} not found",
            )
        return MovieInfoDTO(**doc)

    async def search(
        self,
        genre: str | None = None,
        page_size: int = 50,
        page_number: int = 1,
        sort: str = "imdb_rating",
        title: str | None = None,
    ) -> List[MovieBaseDTO]:
        """
        Получает список фильмов.
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
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")

        return [MovieBaseDTO(**hit) for hit in response]
