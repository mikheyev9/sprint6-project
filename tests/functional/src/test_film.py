import logging
from http import HTTPStatus
from uuid import uuid4
import pytest
from functional.testdata.es_generate.film_generate import MOVIES_DATA


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
logger = logging.getLogger(__name__)

MOVIES_URL = '/films'
MOVIES: list[dict] = MOVIES_DATA.get('movies')

MOVIES_TITLE: list[str] = list(map(lambda movie: movie['title'], MOVIES))

MOVIES_IMDB_RATING: list[str] = list(
    map(lambda movie: movie['imdb_rating'],
        MOVIES)
)


@pytest.mark.parametrize("movie_id", [None, "invalid_id", 99999])
async def test_film_validation(make_get_request, movie_id):
    logger.info(f"Тестирование валидации фильма для movie_id: {movie_id}")
    response_status, _, _ = await make_get_request(
        MOVIES_URL,
        {'id': movie_id} if movie_id else None
    )
    logger.info(f"Статус ответа: {response_status}")
    assert response_status == HTTPStatus.NOT_FOUND


async def test_film_search_existing_id(make_get_request):
    existing_movie = MOVIES[0]
    logger.info(f"Поиск существующего фильма по ID: {existing_movie['id']}")
    response_status, json_response, _ = await make_get_request(
        MOVIES_URL,
        {'id': existing_movie["id"]}
    )
    logger.info(f"Статус ответа: {response_status}, Тело ответа: {json_response}")
    assert response_status == HTTPStatus.OK
    assert json_response == existing_movie


async def test_film_search_existing_title(make_get_request):
    existing_title = MOVIES_TITLE[0]
    logger.info(f"Поиск существующего фильма по заголовку: {existing_title}")
    response_status, json_response, _ = await make_get_request(
        MOVIES_URL,
        {'title': existing_title}
    )
    logger.info(f"Статус ответа: {response_status}, Тело ответа: {json_response}")
    assert response_status == HTTPStatus.OK
    assert json_response['title'] == existing_title


async def test_film_search_nonexistent_title(make_get_request):
    title = 'Несуществующий заголовок фильма'
    logger.info(f"Поиск несущетствующего заголовка фильма: {title}")
    response_status, _, _ = await make_get_request(
        MOVIES_URL,
        {'title': title}
    )
    logger.info(f"Статус ответа: {response_status}")
    assert response_status == HTTPStatus.NOT_FOUND


async def test_get_all_movies(make_get_request):
    logger.info("Получение всех фильмов")
    response_status, json_response, _ = await make_get_request(MOVIES_URL)
    logger.info(f"Статус ответа: {response_status}, Тело ответа: {json_response}")
    assert response_status == HTTPStatus.OK
    assert len(json_response) == len(MOVIES)


async def test_cache_behavior(make_get_request, redis_client):
    existing_movie = MOVIES[0]
    logger.info(f"Тестирование поведения кэша для ID фильма: {existing_movie['id']}")

    response_first_status, json_response_first, _ = await make_get_request(
        MOVIES_URL + "/" + existing_movie["id"],
    )
    logger.info(f"Первый статус ответа: {response_first_status}, Тело ответа: {json_response_first}")
    assert response_first_status == HTTPStatus.OK
    assert json_response_first == existing_movie

    response_second_status, json_response_second, _ = await make_get_request(
        MOVIES_URL,
        {'id': existing_movie["id"]}
    )
    logger.info(f"Второй статус ответа: {response_second_status}, Тело ответа: {json_response_second}")
    assert response_second_status == HTTPStatus.OK
    assert json_response_second == existing_movie

    cached_movie = await redis_client.get(f'film:{existing_movie["id"]}')
    logger.info(f"Закэшированный фильм: {cached_movie}")
    assert cached_movie is not None


@pytest.mark.parametrize("movie_id", [uuid4() for _ in range(5)])
async def test_film_search_random_ids(make_get_request, movie_id):
    logger.info(f"Поиск случайного ID фильма: {movie_id}")
    response_status, _, _ = await make_get_request(
        MOVIES_URL,
        {'id': movie_id}
    )
    logger.info(f"Статус ответа: {response_status}")
    assert response_status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'sort': 'title'}, {
            'status': HTTPStatus.OK,
            'body': sorted(MOVIES_TITLE[:50]),
            'length': 50}),
        ({'sort': 'imdb_rating'}, {
            'status': HTTPStatus.OK,
            'body': sorted(MOVIES_IMDB_RATING[:50]),
            'length': 50}),
    ],
)
async def test_movies_sorting_and_filtering(
    make_get_request,
    query_data,
    expected_answer
):
    logger.info(f"Тестирование сортировки и фильтрации фильмов с параметрами: {query_data}")
    response_status, json_response, _ = await make_get_request(
        MOVIES_URL, query_data
    )
    logger.info(f"Статус ответа: {response_status}, Тело ответа: {json_response}")
    assert response_status == expected_answer['status']


@pytest.mark.parametrize("movie_id", ["", "invalid_uuid", "12345"])
async def test_film_validation_edge_cases(make_get_request, movie_id):
    logger.info(f"Тестирование крайних случаев валидации фильма для movie_id: {movie_id}")
    response_status, _, _ = await make_get_request(
        MOVIES_URL,
        {'id': movie_id} if movie_id else None
    )
    logger.info(f"Статус ответа: {response_status}")
    assert response_status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("title", ["", "A" * 10])
async def test_film_search_title_edge_cases(make_get_request, title):
    logger.info(f"Тестирование крайних случаев поиска заголовка фильма для заголовка: '{title}'")
    response_status, _, _ = await make_get_request(
        MOVIES_URL,
        {'title': title}
    )
    logger.info(f"Статус ответа: {response_status}")
    assert response_status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("query_data", [
    {'sort': 'invalid_sort'},
    {'genre': 'invalid_genre'},
])
async def test_movies_sorting_and_filtering_invalid_params(
    make_get_request,
    query_data
):
    logger.info(f"Тестирование некорректных параметров сортировки и фильтрации: {query_data}")
    response_status, _, _ = await make_get_request(MOVIES_URL, query_data)
    logger.info(f"Статус ответа: {response_status}")
    assert response_status == HTTPStatus.NOT_FOUND  #  HTTPStatus.UNPROCESSABLE_ENTITY
