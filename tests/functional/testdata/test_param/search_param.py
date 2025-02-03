from http import HTTPStatus

from functional.testdata.etl_indexes.movies_indexes import (
    MOVIES_INDEX_MAPPING
)
from functional.testdata.etl_indexes.persons_indexes import (
    PERSONS_INDEX_MAPPING
)
from tests.functional.testdata.es_generate.film_generate import (
    generate_films
)
from tests.functional.testdata.es_generate.genre_generate import (
    generate_persons
)

FILMS_PARAM = [
    'films',
    'films/search/',
    generate_films(),
    MOVIES_INDEX_MAPPING
]

PERSONS_PARAM = [
    'persons',
    'persons/search/',
    generate_persons(),
    PERSONS_INDEX_MAPPING
]

SEARCH_PARAM = [
    [
        {'query': 'The Star'},
        {'status': HTTPStatus.OK, 'length': 50},       
    ]+FILMS_PARAM,
    [
        {},
        {'status': HTTPStatus.OK, 'length': 50},
    ]+FILMS_PARAM,
    [
        {'query': 'Mashed potato'},
        {'status': HTTPStatus.NOT_FOUND, 'length': 1},
    ]+FILMS_PARAM,
    [
        {'query': 'Tom Jerry'},
        {'status': HTTPStatus.OK, 'length': 50},
    ]+PERSONS_PARAM,
    [
        {},
        {'status': HTTPStatus.OK, 'length': 50},
    ]+PERSONS_PARAM,
    [
        {'query': 'Red Boy'},
        {'status': HTTPStatus.NOT_FOUND, 'length': 1},
    ]+PERSONS_PARAM,
]
