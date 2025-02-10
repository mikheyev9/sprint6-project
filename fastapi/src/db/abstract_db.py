from abc import ABC, abstractmethod


class AbstractDAO(ABC):
    """Базовый класс для поиска в БД."""

    @abstractmethod
    async def get(self, table: str, id_obj: str) -> dict[str, str] | None:
        """Получение объекта по id."""
        raise NotImplementedError

    @abstractmethod
    async def search(
            self, table: str,
            query: dict[str, any],
            offset: int = 0,
            limit: int = 50,
            sort: list[dict[str, str]] | None = None,
    ):
        """Поиск объектов в таблице."""
        raise NotImplementedError
