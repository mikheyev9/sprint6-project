from pydantic import Field

from .genre import GenreDTO
from .mixins import UUIDMixin
from .person import PersonInfoDTO


class MovieBaseDTO(UUIDMixin):
    """Базовая информация о фильме."""
    imdb_rating: float | None = Field(default=None)
    title: str


class MovieInfoDTO(MovieBaseDTO):
    """Модель фильма"""
    description: str | None = Field(default=None)
    genres: list[GenreDTO] = Field(default_factory=list)
    directors: list[PersonInfoDTO] | None = Field(default_factory=list)
    actors: list[PersonInfoDTO] = Field(default_factory=list)
    writers: list[PersonInfoDTO] = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list)
    directors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)
