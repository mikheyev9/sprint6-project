import asyncio
import pytest_asyncio

import aiohttp
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from functional.settings import test_settings
from functional.testdata.es_mapping import (
    MOVIES_INDEX_MAPPING,
    PERSONS_INDEX_MAPPING,
    GENRES_INDEX_MAPPING
)


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.elasticsearch_dsn)
    yield es_client
    await es_client.close()

@pytest_asyncio.fixture(name='aiohttp_client', scope='session')
async def aiohttp_client():
    aiohttp_client = aiohttp.ClientSession()
    yield aiohttp_client
    await aiohttp_client.close()
    

@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client):
    async def inner(index: str, es_data: list[dict]):
        data = [{'_index': index, '_id': row['id'], '_source': row} for row in es_data]

        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)

        await es_client.indices.create(index=index, **MOVIES_INDEX_MAPPING)
        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            print(f"Ошибка записи в Elasticsearch: {errors}")
            raise Exception('Ошибка записи данных в Elasticsearch')

        await es_client.indices.refresh(index=index)
        count = await es_client.count(index=index)
        print(f"Записано {count['count']} документов в индекс {index}")

    return inner


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(aiohttp_client):
    async def inner(endpoint: str, query_data: dict = None):
        async with aiohttp_client.get(
            f'{test_settings.service_url}/api/v1/films/{endpoint}/',
            params=query_data
        ) as response:
#            print(response)
#            print(response.status, await response.json())
            return response.status, len(await response.json())       
    return inner
