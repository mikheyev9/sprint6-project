from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, Type, List
from functools import lru_cache

from pydantic import BaseModel

from db.abstract_db import AbstractDAO

T = TypeVar("T", bound=BaseModel)


class BaseService(Generic[T], ABC):
    """
    Базовый сервис для работы с Elasticsearch.
    """

    service_name: str
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        """Автоматически регистрирует все сервисы по `service_name`"""
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "service_name") or not cls.service_name:
            raise TypeError(
                f"Class {cls.__name__} must define a `service_name` attribute."
            )

        BaseService._registry[cls.service_name] = cls

    def __init__(
        self, db: AbstractDAO,
        index: str,
        model: Type[T]
    ):
        self.db = db
        self.index = index
        self.model = model

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Получает объект по ID из Elasticsearch.
        """
        doc = await self.db.get(table=self.index, id_obj=entity_id)
        if doc:
            return self.model(**doc)
        return None

    @abstractmethod
    async def search(self, **kwargs) -> List[T]:
        """
        Поиск объектов в Elasticsearch. Сервисы должны реализовать этот метод.
        """

        pass

    @classmethod
    @lru_cache()
    def get_instance(
        cls,
        service_type: str,
        search_db: AbstractDAO,
    ) -> "BaseService":
        """Возвращает экземпляр сервиса, используя кэширование."""
        service_class = cls._registry.get(service_type)
        if service_class:
            return service_class(search_db)
        raise ValueError(f"Unknown service type: {service_type}")
