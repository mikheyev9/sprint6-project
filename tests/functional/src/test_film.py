import pytest
from http import HTTPStatus
from uuid import uuid4

from functional.testdata.es_generate import MOVIES_DATA


MOVIES_URL = 'films'
MOVIES = MOVIES_DATA.get('movies')

MOVIES_TITLE = [movie['title'] for movie in MOVIES]
MOVIES_IMDB_RATING = [movie['imdb_rating'] for movie in MOVIES]


@pytest.mark.parametrize("movie_id", [None, "недействительный_id", 99999])
async def test_film_validation(make_get_request, movie_id):
    """Тестирование валидации фильма для различных входных значений."""
    url = (
        f"{MOVIES_URL}/{movie_id}"
        if movie_id is not None
        else MOVIES_URL
    )
    response_status, response_data, _ = await make_get_request(url)

    if movie_id is None:
        assert response_status == HTTPStatus.OK, (
            "Ожидали статус OK, когда movie_id не предоставлен."
        )
        assert isinstance(response_data, list), (
            "Ожидали список фильмов в ответе."
        )
    else:
        assert response_status == HTTPStatus.NOT_FOUND, (
            "Ожидали статус NOT_FOUND для недействительного movie_id."
        )
        expected_error = {"detail": "movies not found"}
        assert response_data == expected_error, (
            f"Ожидали {expected_error} в ответе, получили {response_data}."
        )


async def test_film_search_existing_id(make_get_request):
    """ Тестирование поиска существующего фильма по его ID. """
    existing_movie = MOVIES[0]

    response_status, json_response, _ = await make_get_request(
        f"{MOVIES_URL}/{existing_movie['id']}"
    )

    assert response_status == HTTPStatus.OK, (
        "Ожидали статус OK при поиске существующего фильма."
    )
    assert json_response['id'] == existing_movie['id'], (
        "Ожидали совпадение ID фильма."
    )
    assert json_response['title'] == existing_movie['title'], (
        "Ожидали совпадение названия фильма."
    )


async def test_film_search_existing_title(make_get_request):
    """ Тестирование поиска существующего фильма по заголовку. """
    existing_title = MOVIES_TITLE[0]
    response_status, json_response, _ = await make_get_request(
        MOVIES_URL, {'title': existing_title}
    )

    assert response_status == HTTPStatus.OK, (
        "Ожидали статус OK при поиске существующего заголовка."
    )
    assert any(movie['title'] == existing_title for movie in json_response), (
        f"Фильм с заголовком '{existing_title}' не найден."
    )


async def test_get_all_movies(make_get_request):
    """ Тестирование получения всех фильмов. """
    response_status, json_response, _ = await make_get_request(MOVIES_URL)

    assert response_status == HTTPStatus.OK, (
        "Ожидали статус OK при получении всех фильмов."
    )
    assert len(json_response) == len(MOVIES[:50]), (
        "Количество возвращаемых фильмов не совпадает с длиной набора данных.")


async def test_cache_behavior(make_get_request, redis_clean):
    """ Тестирование кэша при одинаковм запросе. """
    await redis_clean()
    existing_movie = MOVIES[0]

    response_first_status, json_response_first, timestamp = (
        await make_get_request(
            f"{MOVIES_URL}/{existing_movie['id']}")
        )

    assert response_first_status == HTTPStatus.OK, (
        "Ожидали статус OK для первого запроса."
    )
    assert json_response_first['id'] == existing_movie['id'], (
        "Ожидали совпадение ID фильма."
    )
    assert json_response_first['title'] == existing_movie['title'], (
        "Ожидали совпадение названия фильма."
    )

    response_second_status, json_response_second, timestamp_redis = (
        await make_get_request(
            f"{MOVIES_URL}/{existing_movie['id']}")
    )
    assert timestamp > timestamp_redis, (
        'Ожидали, что второй запрос вернет данные из кэша Redis, '
        'но, похоже, он был выполнен напрямую из базы данных.'
    )


@pytest.mark.parametrize("movie_id", [uuid4() for _ in range(5)])
async def test_film_search_random_ids(make_get_request, movie_id):
    """ Тестирование поиска фильмов по случайным ID."""
    """ Которые не должны существовать. """
    response_status, _, _ = await make_get_request(
        f"{MOVIES_URL}/{movie_id}"
    )
    assert response_status == HTTPStatus.NOT_FOUND, (
        "Ожидали статус NOT_FOUND для несуществующих ID фильмов."
    )


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'sort': 'imdb_rating'}, {
            'status': HTTPStatus.OK,
            'body': sorted(MOVIES_IMDB_RATING[:50]),
            'length': 50}),
        ({'page': 5},
         {'status': HTTPStatus.OK, 'body': [], 'length': 0}),
        ({'page': 1, 'page_size': 3},
         {'status': HTTPStatus.OK, 'body': sorted(MOVIES_TITLE[:3]),
          'length': 3}),
    ],
)
async def test_movies_sorting_and_filtering(
    make_get_request,
    query_data, expected_answer
):
    """ Тестирование сортировки и фильтрации фильмов с различными params. """
    response_status, json_response, _ = await make_get_request(
        MOVIES_URL,
        query_data
    )

    assert response_status == expected_answer['status'], (
        f"Ожидали статус {expected_answer['status']}, "
        f"получили {response_status}."
    )


@pytest.mark.parametrize("query_data", [
    {'genre': 'недействительный_жанр'},
])
async def test_movies_sorting_and_filtering_invalid_params(
    make_get_request,
    query_data
):
    """ Тестирование поведения при наличии недействительных параметров. """

    response_status, _, _ = await make_get_request(MOVIES_URL, query_data)

    if 'sort' in query_data:
        assert response_status == HTTPStatus.INTERNAL_SERVER_ERROR, (
            "Ожидали внутреннюю ошибку"
            "сервера для недействительных параметров сортировки."
        )
    elif 'genre' in query_data:
        assert response_status == HTTPStatus.NOT_FOUND, (
            'Ожидали статус NOT_FOUND при поиске недействительного жанра.'
        )
    else:
        assert False, 'Неизвестный параметр, не удалось проверить ввод.'
