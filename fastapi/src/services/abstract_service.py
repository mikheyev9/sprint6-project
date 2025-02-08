from abc import ABC, abstractmethod
from typing import TypeVar, List

from pydantic import BaseModel

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class AbstractService(ABC):
    """Абстрактный класс сервиса."""

    @property
    def service_name(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> SchemaType | None:
        """Получить объект из БД."""

    @abstractmethod
    async def search(
        self,
        page_size: int = 50,
        page_number: int = 1,
        query: str | None = None
    ) -> List[SchemaType]:
        """Поиск объектов в БД."""
        raise NotImplementedError
