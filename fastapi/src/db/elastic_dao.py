import logging

from fastapi import Request
from elasticsearch import AsyncElasticsearch, NotFoundError, TransportError
from elasticsearch.exceptions import ConnectionError as ElasticsearchError
from db.abstract_db import AbstractDAO
from utils.backoff import backoff
 
logger = logging.getLogger(__name__)


class ElasticDAO(AbstractDAO):
    """Класс для работы с Elasticsearch."""

    def __init__(self, elastic: AsyncElasticsearch):
        """Конструктор класса."""
        self.elastic = elastic

    @backoff(ElasticsearchError)
    async def get(self, table: str, id_obj: str) -> dict[str, str] | None:
        """Получение объекта по id."""
        try:
            doc = await self.elastic.get(index=table, id=id_obj)
            return doc.get("_source")
        except NotFoundError:
            logger.warning(f"Объект в {table} не найден: id={id_obj}")
        except TransportError as e:
            logger.error(
                f"При запросе id={id_obj} к {table} произошла ошибка: {e}"
            )
        return None

    @backoff(ElasticsearchError)
    async def search(
            self, table: str,
            offset: int = 0,
            limit: int = 50,
            sort: list[dict[str, str]] | None = None,
            filters: dict[str, any] | None = None,
    ):
        """Поиск объектов в таблице."""
        must_conditions = []
        
        filter_conditions = []
        
        if filters is None:
            filters = {}
        
        search_query = {
            "size": limit,
            "from": offset,
            "query": {"bool": {"must": []}},
        }

        for key, value in filters.items():
            if key.count(".") == 1:
                path = key.split(".")[0]
                filter_conditions.append({
                    "nested": {
                        "path": path, "query": {
                            "bool": {"must": [{"match": {key: value}}]}
                        }
                    }
                })
            if key.count(".") == 0:
                must_conditions.append({
                    "multi_match": {"query": value, "fields": [key]}
                })

        if must_conditions:
            search_query["query"]["bool"]["must"] = must_conditions

        if filter_conditions:
            search_query["query"]["bool"]["filter"] = filter_conditions

        if sort:
            search_query["sort"] = sort
        try:
            response = await self.elastic.search(index=table, body=search_query)
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except NotFoundError:
            logger.warning(f"Объекты в {table} не найдены: query={search_query}")
        except TransportError as e:
            logger.error(
                f"При запросе {search_query} к {table} произошла ошибка: {e}"
            )
        return []

 
async def get_elastic(request: Request) -> ElasticDAO:
    """Получение объекта ElasticSearchDB."""
    return request.app.state.elastic
