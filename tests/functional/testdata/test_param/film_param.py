from typing import List

from .dto_param import AbstractDTO
from .genre_param import Genre


class Actor(AbstractDTO):
    id: str
    full_name: str | None


class Director(AbstractDTO):
    id: str
    full_name: str | None


class Writer(AbstractDTO):
    id: str
    full_name: str | None


class Movie(AbstractDTO):
    id: str
    imdb_rating: float | None
    genre: List[Genre]
    title: str | None
    description: str | None
    directors_names: List[str]
    actors_names: List[str]
    writers_names: List[str]
    directors: List[Director]
    actors: List[Actor]
    writers: List[Writer]


class MoviesList(AbstractDTO):
    movies: List[Movie]
