from typing import List
import logging

from elasticsearch import AsyncElasticsearch, NotFoundError
from services.base_service import BaseService
from models.genre import GenresDTO, GenreDTO

logger = logging.getLogger(__name__)


class GenreService(BaseService[GenresDTO]):
    """Сервис для работы с жанрами в Elasticsearch."""

    service_name = "genre"
    page_size = 50

    def __init__(self, elastic: AsyncElasticsearch):
        super().__init__(elastic, index="genres", model=GenreDTO)

    async def search(self) -> List[GenreDTO]:
        """
        Возвращает список всех жанров из Elasticsearch.
        """

        search_query = {
            "size": self.page_size,
            "query": {"match_all": {}}
        }

        try:
            print(search_query)
            response = await self.elastic.search(
                index=self.index,
                body=search_query
            )
            return [
                self.model(
                    **hit["_source"]
                ) for hit in response["hits"]["hits"]
            ]

        except NotFoundError:
            logger.warning("Жанры не найдены.")
            return []

        except Exception as e:
            logger.error(f"Ошибка при запросе жанров из Elasticsearch: {e}")
            return []
