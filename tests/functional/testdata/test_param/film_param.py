from abc import ABC
from typing import List, Optional, Type, Dict
from pydantic import BaseModel, ConfigDict


class Biulder(ABC):
    __subclasses: Dict[str, Type['Biulder']] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__subclasses[cls.__name__.lower()] = cls

    @classmethod
    def get_subclasses(cls):
        return cls.__subclasses


class AbstractDTO(BaseModel, Biulder):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )


class Genre(AbstractDTO):
    id: str
    name: Optional[str]


class Actor(AbstractDTO):
    id: str
    full_name: Optional[str]


class Director(AbstractDTO):
    id: str
    full_name: Optional[str]


class Writer(AbstractDTO):
    id: str
    full_name: Optional[str]


class Movie(AbstractDTO):
    id: str
    imdb_rating: Optional[float]
    genre: List[Genre]
    title: Optional[str]
    description: Optional[str]
    directors_names: List[str]
    actors_names: List[str]
    writers_names: List[str]
    directors: List[Director]
    actors: List[Actor]
    writers: List[Writer]


class PersonFilm(AbstractDTO):
    id: str
    roles: List[str]


class MoviesList(AbstractDTO):
    movies: List[Movie]


class Person(AbstractDTO):
    id: str
    full_name: Optional[str]
    films: List[PersonFilm]


class PersonsList(AbstractDTO):
    persons: List[Person]


class GenresList(AbstractDTO):
    genres: List[Genre]
