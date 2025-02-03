import pytest

from tests.functional.testdata.test_param.search_param import SEARCH_PARAM

@pytest.mark.parametrize(
    'query_data, expected_answer, index, endpoint, generate, map',
    SEARCH_PARAM
)
@pytest.mark.asyncio
async def test_films_search(
    es_write_data, make_get_request, redis_clean,
    query_data, expected_answer, index, endpoint, generate, map
): 
    await redis_clean()
    await es_write_data(
        index, generate, map
    )
    status, body_count, timestamp1 = await make_get_request(
        endpoint, query_data
    )
    assert status == expected_answer['status'], (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ с кодом {expected_answer['status']}.'
    )
    assert body_count == expected_answer['length'], (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает в ответе нужное количество {expected_answer['length']}.'
    )
    status, body_count, timestamp2 = await make_get_request(
        endpoint, query_data
    )
    assert status == expected_answer['status'], (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ с кодом {expected_answer['status']}.'
    )
    assert body_count == expected_answer['length'], (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает в ответе нужное количество {expected_answer['length']}.'
    )
    assert timestamp1 > timestamp2, (
        f'Проверьте, что get-запрос к `/api/v1/{endpoint}` '
        f'возвращает ответ из кеш Redis.'
    )
