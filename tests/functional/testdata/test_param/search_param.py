from http import HTTPStatus

from functional.testdata.etl_indexes.movies_indexes import (
    MOVIES_INDEX_MAPPING
)
from functional.testdata.etl_indexes.persons_indexes import (
    PERSONS_INDEX_MAPPING
)


FILMS_PARAM = [
    'movies',
    'films/search/',
    "films.json",
    MOVIES_INDEX_MAPPING
]

PERSONS_PARAM = [
    'persons',
    'persons/search/',
    "persons.json",
    PERSONS_INDEX_MAPPING
]

SEARCH_PARAM = [
    [
        {'query': 'Star'},
        {'status': HTTPStatus.OK, 'length': 50},       
    ]+FILMS_PARAM,
    [
        {'query': 'Star', 'page_size': 60},
        {'status': HTTPStatus.OK, 'length': 60},       
    ]+FILMS_PARAM,
    [
        {'query': 'Star', 'page_number': 2},
        {'status': HTTPStatus.OK, 'length': 10},       
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
        {'query': 'Marya Gant'},
        {'status': HTTPStatus.OK, 'length': 1},
    ]+PERSONS_PARAM,
    [
        {'query': 'M', 'page_size': 2},
        {'status': HTTPStatus.OK, 'length': 2},
    ]+PERSONS_PARAM,
    [
        {'query': 'Michael', 'page_number': 2, 'page_size': 5},
        {'status': HTTPStatus.OK, 'length': 3},
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