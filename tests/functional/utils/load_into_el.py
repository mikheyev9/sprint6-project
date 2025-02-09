import json
import os
from elasticsearch import Elasticsearch, helpers


def load_data_to_elasticsearch():
    es_host = 'http://localhost:9200'
    indices = ['genres', 'movies', 'persons']
    es = Elasticsearch([es_host])

    input_dir = 'tests/functional/json_data'

    for index in indices:
        filename = os.path.join(input_dir, f"{index}.json")

        if os.path.exists(filename):
            with open(filename, 'r') as json_file:
                data = json.load(json_file)

                actions = [
                    {
                        "_index": index,
                        "_source": doc
                    }
                    for doc in data[index]
                ]

                helpers.bulk(es, actions)
                print(f"Данные из {filename} успешно загружены в индекс {index}.")
        else:
            print(f"Файл {filename} не найден.")


# load_data_to_elasticsearch()
