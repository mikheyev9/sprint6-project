

import pytest

from functional.testdata.es_generate import generate_film_search
from functional.settings import test_settings

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(
    es_write_data, make_get_request,
    query_data,
    expected_answer
): 
    await es_write_data(
        test_settings.elasticsearch_index,
        generate_film_search()
    )
    status, body_count = await make_get_request('search', query_data)
    assert status == expected_answer['status']
    assert body_count == expected_answer['length']