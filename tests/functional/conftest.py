import asyncio
import time

import pytest_asyncio
from redis import asyncio as aioredis

import aiohttp
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from functional.settings import test_settings


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


@pytest_asyncio.fixture(name='redis_client', scope='session')
async def redis__client():
    redis_client = aioredis.from_url(test_settings.redis_dsn)
    yield redis_client
    await redis_client.aclose()


@pytest_asyncio.fixture(name='redis_clean')
def redis_clean(redis_client):
    async def inner():
        await redis_client.flushall()
        count_keys = await redis_client.dbsize()
        if count_keys != 0:
            print("Кеш в Redis не пустой")
            raise Exception(f"Ошибка: ключей Redis:{count_keys} больше 0.")
        print(f"Redis готов к тестам. Кол-во ключей:{count_keys}.")
    return inner


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client):
    async def inner(index: str, es_data: list[dict], model_index):
        data = [{'_index': index, '_id': row['id'], '_source': row} for row in es_data]

        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)

        await es_client.indices.create(index=index, **model_index)
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
        time_start = time.time()
        async with aiohttp_client.get(
            f'{test_settings.service_url}/api/v1/{endpoint}',
            params=query_data
        ) as response:
            return (
                response.status,
                len(await response.json()),
                time.time() - time_start
            )
    return inner
