from typing import List
import logging

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

        search_query = {"match_all": {}}

        response = await self.db.search(
            table=self.index,
            query=search_query,
            limit=self.page_size,
        )
        return [GenreDTO(**hit) for hit in response]
