from http import HTTPStatus # noqa
from uuid import uuid4 # noqa

import pytest # noqa
from tests.functional.settings import test_settings # noqa
from tests.functional.testdata.es_generate.film_generate import MOVIES_DATA # noqa

MOVIES: list[dict] = MOVIES_DATA.get('movies')

MOVIES_TITLE: list[str] = list(map(lambda movie: movie['title'], MOVIES))
MOVIES_IMDB_RATING: list[str] = list(
    map(lambda movie: movie['imdb_rating'], MOVIES)
)
MOVIES_GENRE: list[dict] = list(map(lambda movie: movie['genre']))
