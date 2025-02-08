from abc import abstractmethod
from typing import Generic, Type, List
from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError

from services.abstract_service import SchemaType, AbstractService


class BaseService(Generic[SchemaType], AbstractService):
    """
    Базовый сервис для работы с Elasticsearch.
    """

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
        self, elastic: AsyncElasticsearch,
        index: str,
        model: Type[SchemaType]
    ):
        self.elastic = elastic
        self.index = index
        self.model = model

    async def get_by_id(self, entity_id: str) -> SchemaType | None:
        """
        Получает объект по ID из Elasticsearch.
        """

        try:
            doc = await self.elastic.get(index=self.index, id=entity_id)
            return self.model(**doc["_source"])
        except NotFoundError:
            return None

    @abstractmethod
    async def search(
        self,
        page_size: int = 50,
        page_number: int = 1,
        query: str | None = None,
        *args,
        **kwargs,
    ) -> List[SchemaType]:
        """Поиск объектов в БД."""
        raise NotImplementedError

    @classmethod
    @lru_cache()
    def get_instance(
        cls,
        service_type: str,
        elastic: AsyncElasticsearch
    ) -> "BaseService":
        """Возвращает экземпляр сервиса, используя кэширование."""
        service_class = cls._registry.get(service_type)
        if service_class:
            return service_class(elastic)
        raise ValueError(f"Unknown service type: {service_type}")
