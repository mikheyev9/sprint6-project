import logging
import json
from elasticsearch import Elasticsearch, ConnectionError


logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


class ElasticsearchUtils:
    def __init__(self, hosts):
        self.es = Elasticsearch(hosts)

    def check_connection(self):
        if not self.es.ping():
            logging.warning(
                "Подключение к Elasticsearch не установлено. "
                "Используем текущие JSON-файлы."
            )
            return False
        logging.info("Соединение с Elasticsearch установлено.")
        return True

    def export_data(self, indices):
        if not self.check_connection():
            raise ConnectionError(
                "Подключение к Elasticsearch не установлено."
            )

        for index in indices:
            logging.info(f"Извлекаем данные из индекса '{index}'...")

            try:
                query = {"query": {"match_all": {}}}
                response = self.es.search(index=index, body=query, size=10000)
                data = {index: [hit['_source'] for hit in response[
                    'hits']['hits']
                    ]
                }

                filename = f"{index}.json"
                with open(filename, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, indent=4)

                logging.info(
                    f"Данные из индекса '{index}' "
                    f"успешно выгружены в {filename}."
                )
            except Exception as e:
                logging.error(
                    f"Ошибка при выгрузке из индекса '{index}': {str(e)}"
                )
