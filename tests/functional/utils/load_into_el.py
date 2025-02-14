import json
import os
import asyncio
import logging

from elasticsearch import AsyncElasticsearch, helpers  # noqa
from elasticsearch.helpers import BulkIndexError

from functional.testdata.etl_indexes.genres_indexes import GENRES_INDEX_MAPPING
from functional.testdata.etl_indexes.movies_indexes import MOVIES_INDEX_MAPPING
from functional.testdata.etl_indexes.persons_indexes import PERSONS_INDEX_MAPPING
from functional.settings import test_settings

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


async def create_index_if_not_exists(es, index_name, mapping):
    if await es.indices.exists(index=index_name):
        await es.indices.delete(index=index_name)
        logger.info(f"Индекс '{index_name}' удалён.")
    await es.indices.create(index=index_name, body=mapping)
    logger.info(f"Индекс '{index_name}' создан.")


async def load_data_to_elasticsearch():
    es_host = test_settings.elasticsearch_dsn
    indices = {
        'genres': GENRES_INDEX_MAPPING,
        'movies': MOVIES_INDEX_MAPPING,
        'persons': PERSONS_INDEX_MAPPING
    }

    es = AsyncElasticsearch([es_host])
    input_dir = 'functional/json_data'

    for index, mapping in indices.items():
        await create_index_if_not_exists(es, index, mapping)

        filename = os.path.join(input_dir, f"{index}.json")

        if os.path.exists(filename):
            with open(filename, 'r') as json_file:
                data = json.load(json_file)

                for doc in data[index]:
                    doc['_id'] = doc['id']
                try:
                    await helpers.async_bulk(
                        es,
                        index=index,
                        actions=data[index],
                        chunk_size=10000
                    )
                    logger.info(
                        f"Данные из {filename} успешно загружены "
                        f"в индекс {index}."
                        )
                except BulkIndexError as e:
                    print(f"Ошибка индексации: {e}")
                    for error in e.errors:
                        doc_id = error.get('_id', 'неизвестно')
                        print(f"Ошибка для документа (ID: {doc_id})")
        else:
            print(f"Файл {filename} не найден.")

    await es.close()

asyncio.run(load_data_to_elasticsearch())
