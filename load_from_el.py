import json
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://localhost:9200'],
)

indices = ['genres', 'movies', 'persons']

for index in indices:
    query = {
        "query": {
            "match_all": {}
        }
    }

    response = es.search(index=index, body=query, size=10000)

    data = {index: [hit['_source'] for hit in response['hits']['hits']]}

    filename = f"{index}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Данные из индекса '{index}' успешно выгружены в {filename}.")
