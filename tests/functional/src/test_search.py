import pytest

from tests.functional.testdata.test_param.search_param import SEARCH_PARAM


@pytest.mark.parametrize(
    'query_data, expected_answer, index, endpoint',
    SEARCH_PARAM
)
@pytest.mark.asyncio
async def test_films_search(
    make_get_request, redis_clean,
    query_data, expected_answer, index, endpoint
):
    """
    Тестирование endpoints 'search' для индексов movies, persons
    с указанием существуего, не существуещего или отсутствуещего
    слова для поиска с различными параметрами страницы.
    """
    await redis_clean()
    status, body, timestamp = await make_get_request(
        endpoint, query_data
    )
    assert status == expected_answer['status'], (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ с кодом {expected_answer['status']}.'
    )
    assert len(body) == expected_answer['length'], (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        'возвращает в ответе нужное количество '
        f'{index}:{expected_answer['length']}.'
    )
    if expected_answer['status'] == 200:
        status_redis, body_redis, timestamp_redis = await make_get_request(
            endpoint, query_data
        )
        assert timestamp > timestamp_redis, (
            f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
            f'возвращает ответ из кеш Redis.'
        )
        assert status_redis == expected_answer['status'], (
            f'Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` '
            f'возвращает ответ с кодом {expected_answer['status']}.'
        )
        assert len(body_redis) == expected_answer['length'], (
            f'Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` '
            'возвращает в ответе нужное количество '
            f'{index}:{expected_answer['length']}.'
        )
        assert body == body_redis, (
            f'Проверьте, что get-запрос в Redis к `/api/v1/{endpoint}` '
            f'возвращает ответ, как в get-запросе в ElasticSearch.'
        )
