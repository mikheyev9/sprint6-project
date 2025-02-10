from typing import List, Optional
import logging

from db.abstract_db import AbstractDAO
from models.person import PersonInfoDTO
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class PersonService(BaseService[PersonInfoDTO]):
    """Сервис для работы с данными о персонах в Elasticsearch."""

    service_name = "person"

    def __init__(self, search_db: AbstractDAO):
        super().__init__(search_db, index="persons", model=PersonInfoDTO)

    async def search(
        self,
        page_size: int = 50,
        page_number: int = 1,
        full_name: Optional[str] = None
    ) -> List[PersonInfoDTO]:
        """
        Выполняет поиск персон по имени.
        """
        filters = {}
        if full_name:
            filters["full_name"] = full_name
        response = await self.db.search(
            table=self.index,
            limit=page_size,
            offset=(page_number - 1) * page_size,
            filters=filters,
        )
        return [self.model(**hit) for hit in response]
