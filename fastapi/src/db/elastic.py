import logging

from fastapi import Request
from elasticsearch import AsyncElasticsearch, NotFoundError, TransportError

from db.abstract_db import AbstractDB

logger = logging.getLogger(__name__)


class ElasticDB(AbstractDB):
    """Класс для работы с Elasticsearch."""

    def __init__(self, elastic: AsyncElasticsearch):
        """Конструктор класса."""
        self.elastic = elastic

    async def get(self, table: str, id_obj: str) -> dict[str, str] | None:
        """Получение объекта по id."""
        try:
            doc = await self.elastic.get(index=table, id=id_obj)
        except NotFoundError:
            logger.warning(f"Объект в {table} не найден: id={id_obj}")
            return None
        return doc.get("_source")

    async def search(
            self, table: str,
            query: dict[str, any],
            offset: int = 0,
            limit: int = 50,
            sort: list[dict[str, str]] | None = None,
    ):
        """Поиск объектов в таблице."""
        search_query = {
            "size": limit,
            "from": offset,
            "query": query,
        }
        if sort:
            search_query["sort"] = sort
        try:
            return await self.elastic.search(index=table, body=search_query)
        except NotFoundError:
            logger.warning(f"Объекты в {table} не найдены: query={query}")
            return []
        except TransportError as e:
            logger.error(
                f"При запросе {query} к {table} произошла ошибка: {e}"
            )
            return []


async def get_elastic(request: Request) -> ElasticDB:
    """Получение объекта ElasticSearchDB."""
    return ElasticDB(request.app.state.elastic)
