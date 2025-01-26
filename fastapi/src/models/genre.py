from pydantic import Field

from .mixins import UUIDMixin
from .dto import AbstractDTO


class GenreDTO(UUIDMixin):
    """Модель жанра"""
    name: str = Field(default_factory=str)


class GenresDTO(AbstractDTO):
    """Модель жанров"""
    genres: list[GenreDTO] = Field(default_factory=str)
