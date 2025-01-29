from pydantic import Field
from .mixins import UUIDMixin
from .dto import AbstractDTO
from uuid import UUID, uuid4


class GenreDTO(UUIDMixin):
    """Модель жанров"""
    name: str = Field(default_factory=str)


class MoviesGenreDTO(AbstractDTO):
    "Модель жанров для Movies"
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(default_factory=str)
