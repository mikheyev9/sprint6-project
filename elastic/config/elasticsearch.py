import logging
from logging import config as logging_config

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from utils.backoff import backoff
from .base import BaseConfig
from utils.logger import LOGGING_CONFIG

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


class ElasticsearchClient(BaseConfig):
    """Класс для работы с Elasticsearch."""

    @backoff(ConnectionError)
    def reconnect(self):
        """Подключение к Elasticsearch."""
        logger.info('Попытка подключения к Elasticsearch с dsn: %s', self.dsn)
        return Elasticsearch(str(self.dsn))
