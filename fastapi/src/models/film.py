from pydantic import Field

from .genre import GenreDTO
from .mixins import UUIDMixin
from .person import PersonInfoDTO


class MovieBaseDTO(UUIDMixin):
    """Базовая информация о фильме."""
    title: str
    imdb_rating: float | None = Field(default=None)


class MovieInfoDTO(MovieBaseDTO):
    """Модель фильма"""
    description: str | None = Field(default=None)
    genres: list[GenreDTO] = Field(default_factory=list)
    actors: list[PersonInfoDTO] = Field(default_factory=list)
    writers: list[PersonInfoDTO] = Field(default_factory=list)
    directors: list[PersonInfoDTO] | None = Field(default_factory=list)
