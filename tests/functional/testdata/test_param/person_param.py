from typing import List

from .dto_param import AbstractDTO


class PersonFilm(AbstractDTO):
    id: str
    roles: List[str]


class Person(AbstractDTO):
    id: str
    full_name: str | None
    films: List[PersonFilm]


class PersonsList(AbstractDTO):
    persons: List[Person]
