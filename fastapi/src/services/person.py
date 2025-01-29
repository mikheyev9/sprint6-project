from typing import List, Optional
import logging

from elasticsearch import AsyncElasticsearch, NotFoundError
from models.person import PersonInfoDTO
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class PersonService(BaseService[PersonInfoDTO]):
    """Сервис для работы с данными о персонах в Elasticsearch."""

    service_name = "person"

    def __init__(self, elastic: AsyncElasticsearch):
        super().__init__(elastic, index="persons", model=PersonInfoDTO)


    async def search(
        self, 
        page_size: int = 50, 
        page_number: int = 1, 
        query: Optional[str] = None
    ) -> List[PersonInfoDTO]:
        """
        Выполняет поиск персон по имени.
        """
        
        search_query = {
            "size": page_size,
            "from": (page_number - 1) * page_size,
            "query": {"bool": {"must": []}}
        }

        if query:
            search_query["query"]["bool"]["must"].append(
                {"multi_match": {"query": query, "fields": ["name"]}}
            )

        try:
            response = await self.elastic.search(index=self.index, body=search_query)
            return [self.model(**hit["_source"]) for hit in response["hits"]["hits"]]
        
        except NotFoundError:
            logger.warning(f"Персоны не найдены. Запрос: query={query}")
            return []
        
        except Exception as e:
            logger.error(f"Ошибка при запросе к Elasticsearch: {e}")
            return []

