import pytest
from http import HTTPStatus

from functional.testdata.es_generate import PERSONS_DATA


PERSONS = PERSONS_DATA.get('persons')


@pytest.mark.parametrize("endpoint", ["persons/0", "persons/0/film"])
@pytest.mark.asyncio
async def test_person_not_found(make_get_request, endpoint):
    """Проверяем, что 404 ошибка возвращается."""
    status, body, timestamp = await make_get_request(endpoint)
    assert status == HTTPStatus.NOT_FOUND, (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ с кодом 404.'
    )
    assert "detail" in body.keys(), (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает описание ошибки.'
    )


@pytest.mark.asyncio
async def test_person(make_get_request, redis_clean):
    """Проверка ответа о персоне."""
    endpoint = f"persons/{PERSONS[0]['id']}"
    await redis_clean()
    status, body, timestamp = await make_get_request(endpoint)
    assert status == HTTPStatus.OK, (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ с кодом 200.'
    )
    assert body.get("full_name") == PERSONS[0]["full_name"], (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает правильные данные.'
    )
    assert "films" in body.keys(), (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ с данными о фильмах.'
    )
    assert len(body.get("films")) == len(PERSONS[0]["films"]), (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает правильное количество фильмов.'
    )
    status_redis, body_redis, timestamp_redis = await make_get_request(endpoint)
    assert timestamp > timestamp_redis, (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ из кеш Redis.'
    )
    assert status_redis == HTTPStatus.OK, (
        f'Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` '
        f'возвращает ответ с кодом 200.'
    )
    assert body == body_redis, (
        f'Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` '
        f'возвращает ответ, как в get-запросе в ElasticSearch.'
    )

@pytest.mark.asyncio
async def test_person_film(make_get_request, redis_clean):
    """Проверка ответа о фильмах персоны."""
    endpoint = f"persons/{PERSONS[0]['id']}/film"
    await redis_clean()
    status, body, timestamp = await make_get_request(endpoint)
    assert status == HTTPStatus.OK, (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ с кодом 200.'
    )
    assert isinstance(body, list), (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает список.'
    )
    assert len(body) == len(PERSONS[0]["films"]), (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает правильное количество фильмов.'
    )
    status_redis, body_redis, timestamp_redis = await make_get_request(endpoint)
    assert timestamp > timestamp_redis, (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ из кеш Redis.'
    )
    assert status_redis == HTTPStatus.OK, (
        f'Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` '
        f'возвращает ответ с кодом 200.'
    )
    assert body == body_redis, (
        f'Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` '
        f'возвращает ответ, как в get-запросе в ElasticSearch.'
    )
