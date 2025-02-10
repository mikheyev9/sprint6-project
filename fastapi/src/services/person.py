from typing import List, Optional
import logging

from db.abstract_db import AbstractDB
from models.person import PersonInfoDTO
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class PersonService(BaseService[PersonInfoDTO]):
    """Сервис для работы с данными о персонах в Elasticsearch."""

    service_name = "person"

    def __init__(self, search_db: AbstractDB):
        super().__init__(search_db, index="persons", model=PersonInfoDTO)

    async def search(
        self,
        page_size: int = 50,
        page_number: int = 1,
        query: Optional[str] = None
    ) -> List[PersonInfoDTO]:
        """
        Выполняет поиск персон по имени.
        """

        search_query = {"bool": {"must": []}}

        if query:
            search_query["bool"]["must"].append(
                {"multi_match": {"query": query, "fields": ["full_name"]}}
            )

        response = await self.search_db.search(
            table=self.index,
            query=search_query,
            limit=page_size,
            offset=(page_number - 1) * page_size,
        )
        return [self.model(**hit) for hit in response]
