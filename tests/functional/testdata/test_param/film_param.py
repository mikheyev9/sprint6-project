from typing import List, Optional

from .dto_param import AbstractDTO
from .genre_param import Genre


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


class MoviesList(AbstractDTO):
    movies: List[Movie]
