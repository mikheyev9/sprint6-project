from http import HTTPStatus

FILMS_PARAM = [
    'movies',
    'films/search/',
]

PERSONS_PARAM = [
    'persons',
    'persons/search/',
]

SEARCH_PARAM = [
    [
        {'query': 'The Star'},
        {'status': HTTPStatus.OK, 'length': 50},
    ]+FILMS_PARAM,
    [
        {'query': 'The Star', 'page_size': 60},
        {'status': HTTPStatus.OK, 'length': 60},
    ]+FILMS_PARAM,
    [
        {'query': 'The Star', 'page_number': 20},
        {'status': HTTPStatus.OK, 'length': 49},
    ]+FILMS_PARAM,
    [
        {},
        {'status': HTTPStatus.OK, 'length': 50},
    ]+FILMS_PARAM,
    [
        {'query': 'NoneFilms'},
        {'status': HTTPStatus.NOT_FOUND, 'length': 1},
    ]+FILMS_PARAM,
    [
        {'query': 'John'},
        {'status': HTTPStatus.OK, 'length': 50},
    ]+PERSONS_PARAM,
    [
        {'query': 'John', 'page_size': 60},
        {'status': HTTPStatus.OK, 'length': 60},
    ]+PERSONS_PARAM,
    [
        {'query': 'John', 'page_number': 2},
        {'status': HTTPStatus.OK, 'length': 20},
    ]+PERSONS_PARAM,
    [
        {},
        {'status': HTTPStatus.OK, 'length': 50},
    ]+PERSONS_PARAM,
    [
        {'query': 'NonePerson'},
        {'status': HTTPStatus.NOT_FOUND, 'length': 1},
    ]+PERSONS_PARAM,
]
