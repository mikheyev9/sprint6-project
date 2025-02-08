import json
from elasticsearch import Elasticsearch


def export_elasticsearch_data():
    es_host = 'http://localhost:9200'
    indices = ['genres', 'movies', 'persons']
    es = Elasticsearch([es_host])
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
