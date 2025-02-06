from http import HTTPStatus

import pytest

from tests.functional.testdata.test_param.person_param import PERSONS_PARAM, PERSONS_PARAM_FILM
from functional.testdata.etl_indexes.persons_indexes import PERSONS_INDEX_MAPPING
from functional.testdata.etl_indexes.movies_indexes import MOVIES_INDEX_MAPPING


@pytest.mark.parametrize("endpoint, expected_answer", PERSONS_PARAM)
@pytest.mark.asyncio
async def test_person(
    es_write_data, make_get_request, redis_clean, endpoint, expected_answer
):
    """Проверка работы get-запроса к `/api/v1/person/{person_id}`."""
    await redis_clean()
    await es_write_data("persons", "persons.json", PERSONS_INDEX_MAPPING)

    status, body, timestamp = await make_get_request(endpoint)
    assert status == HTTPStatus.OK, (
        f"Проверьте, что get-запрос к `/api/v1/{endpoint}` "
        f"возвращает ответ с кодом {expected_answer['status']}."
    )

    assert body.get("id") == expected_answer["id"], (
        f"Проверьте, что get-запрос к `/api/v1/{endpoint}` "
        f"возвращает ответ с id {expected_answer['id']}."
    )
    assert body.get("full_name") == expected_answer["full_name"], (
        f"Проверьте, что get-запрос к `/api/v1/{endpoint}` "
        f"возвращает ответ с full_name {expected_answer['full_name']}."
    )
    assert len(body.get("films")) == expected_answer["film_count"], (
        f"Проверьте, что get-запрос к `/api/v1/{endpoint}` "
        f"возвращает ответ с количеством фильмов {expected_answer['film_count']}."
    )

    status_redis, body_redis, timestamp_redis = await make_get_request(endpoint)
    assert timestamp > timestamp_redis, (
        f"Проверьте, что get-запрос к `/api/v1/{endpoint}` "
        f"возвращает ответ из кеш Redis."
    )

    assert status_redis == HTTPStatus.OK, (
        f"Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` "
        f"возвращает ответ с кодом 200."
    )

    assert body == body_redis, (
        f"Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` "
        f"возвращает ответ, как в get-запросе в ElasticSearch."
    )


@pytest.mark.asyncio
async def test_person_not_found(es_write_data, make_get_request, redis_clean):
    """Проверка работы get-запроса к `/api/v1/person/{person_id}` с отсутствием персонажа."""
    await redis_clean()
    await es_write_data("persons", "persons.json", PERSONS_INDEX_MAPPING)
    status, body, timestamp = await make_get_request('persons/0')
    assert status == HTTPStatus.NOT_FOUND, (
        f"Проверьте, что get-запрос к `/api/v1/persons/0` "
        f"возвращает ответ с кодом {HTTPStatus.NOT_FOUND}."
    )


@pytest.mark.parametrize("endpoint, expected_answer", PERSONS_PARAM_FILM)
@pytest.mark.asyncio
async def test_person_film(
    es_write_data, make_get_request, redis_clean, endpoint, expected_answer
):
    """Проверка работы get-запроса к `/api/v1/person/{person_id}/film`."""
    await redis_clean()
    await es_write_data("movies", "films.json", MOVIES_INDEX_MAPPING)
    status, body, timestamp = await make_get_request(endpoint)

    assert status == HTTPStatus.OK, (
        f"Проверьте, что get-запрос к `/api/v1/persons/person_id/film` "
        f"возвращает ответ с кодом {HTTPStatus.OK}."
    )

    assert len(body) == expected_answer["count"], (
        f"Проверьте, что get-запрос к `/api/v1/{endpoint}` "
        f"возвращает ответ с количеством фильмов {expected_answer["count"]}."
    )

    assert body[0] == expected_answer["first_film"], (
        f"Проверьте, что get-запрос к `/api/v1/{endpoint}` "
        f"возвращает ответ с первым фильмом {expected_answer['first_film']}."
    )

    status_redis, body_redis, timestamp_redis = await make_get_request(endpoint)
    assert timestamp > timestamp_redis, (
        f"Проверьте, что get-запрос к `/api/v1/{endpoint}` "
        f"возвращает ответ из кеш Redis."
    )

    assert status_redis == HTTPStatus.OK, (
        f"Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` "
        f"возвращает ответ с кодом 200."
    )

    assert body == body_redis, (
        f"Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` "
        f"возвращает ответ, как в get-запросе в ElasticSearch."
    )


@pytest.mark.asyncio
async def test_person_film_not_found(es_write_data, make_get_request, redis_clean):
    """Проверка работы get-запроса к `/api/v1/person/{person_id}/film` с отсутствием персонажа."""
    await redis_clean()
    await es_write_data("movies", "films.json", MOVIES_INDEX_MAPPING)
    status, body, timestamp = await make_get_request('persons/0/film')
    assert status == HTTPStatus.NOT_FOUND, (
        f"Проверьте, что get-запрос к `/api/v1/persons/0` "
        f"возвращает ответ с кодом {HTTPStatus.NOT_FOUND}."
    )
