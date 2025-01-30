from typing import List, Optional

from pydantic import Field

from .mixins import UUIDMixin
from .dto import AbstractDTO


class GenreDTO(UUIDMixin):
    """Модель жанра"""
    name: Optional[str] = Field(default=None)


class GenresDTO(AbstractDTO):
    """Модель списка жанров"""
    genres: List[GenreDTO] = Field(default_factory=list)
