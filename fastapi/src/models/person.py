from typing import List
from pydantic import Field

from .mixins import UUIDMixin
from .dto import AbstractDTO


class FilmDTO(UUIDMixin):
    """Модель фильма."""

    roles: List[str] = Field(default_factory=list)


class PersonInfoDTO(UUIDMixin):
    """Модель информации о человеке."""

    name: str = Field(default_factory=str)
    films: List[FilmDTO] = Field(default_factory=list)


class PersonsDTO(AbstractDTO):
    persons: list[PersonInfoDTO] = Field(default_factory=list)
