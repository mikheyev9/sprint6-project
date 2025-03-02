import time

from elasticsearch import Elasticsearch
from functional.settings import elasticsearch_settings

if __name__ == "__main__":
    es_client = Elasticsearch(hosts=elasticsearch_settings.dsn)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
