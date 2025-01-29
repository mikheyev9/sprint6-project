from pydantic import Field

from .genre import GenreDTO
from .mixins import UUIDMixin
from .person import PersonDTO


class MovieBaseDTO(UUIDMixin):
    """Базовая информация о фильме."""
    title: str
    imdb_rating: float | None = Field(default=None)


class MovieInfoDTO(MovieBaseDTO):
    """Модель фильма"""
    description: str | None = Field(default=None)
    genres: list[str] = Field(default_factory=list)
    actors: list[PersonDTO] = Field(default_factory=list)
    writers: list[PersonDTO] = Field(default_factory=list)
    directors: list[PersonDTO] | None = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list)
    directors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)