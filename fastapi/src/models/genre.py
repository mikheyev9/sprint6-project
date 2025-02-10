from typing import List

from pydantic import Field

from .mixins import UUIDMixin
from .dto import AbstractDTO


class GenreDTO(UUIDMixin):
    """Модель жанра"""
    name: str | None = Field(default=None, examples=['Comedy'])


class GenresDTO(AbstractDTO):
    """Модель списка жанров"""
    genres: List[GenreDTO] = Field(default_factory=list)
