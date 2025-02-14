from typing import List

from .dto_param import AbstractDTO


class Genre(AbstractDTO):
    id: str
    name: str | None


class GenresList(AbstractDTO):
    genres: List[Genre] | None
