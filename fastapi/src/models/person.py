from pydantic import Field

from .mixins import UUIDMixin


class FilmDTO(UUIDMixin):
    """Модель фильма."""

    roles: list[str] = Field(default_factory=list)


class PersonInfoDTO(UUIDMixin):
    """Модель информации о человеке."""

    name: str = Field(default_factory=str)
    films: list[FilmDTO] = Field(default_factory=list)
