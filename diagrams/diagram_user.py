from diagrams import Cluster, Diagram, Edge
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.client import User
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import FastAPI

# Настройки графа
graph_attr = {"fontsize": "20", "pad": "1", "dpi": "300", "splines": "ortho"}  # Улучшает визуализацию соединений

with Diagram("diagram_user", direction="LR", graph_attr=graph_attr):
    # Основные компоненты
    client = User("Клиент")
    nginx = Nginx("Nginx")

    # Кэш и базы данных
    redis = Redis("Redis")

    # Сервис авторизации
    with Cluster("Сервис авторизации"):
        auth_api = FastAPI("Auth API")
        auth_db = PostgreSQL("PostgresAuth")
        auth_api >> auth_db  # Связь внутри кластера

    # Сервис поиска фильмов
    with Cluster("Сервис поиска фильмов"):
        search_api = FastAPI("Search API")
        elastic = Elasticsearch("ElasticSearch")
        search_api >> elastic  # Связь внутри кластера

    # Главный поток запросов
    client >> Edge(label="Запрос") >> nginx >> Edge(label="Ответ") >> client
    nginx >> auth_api
    auth_api >> nginx >> search_api

    # Поиск данных в Redis
    search_api >> redis
    redis >> Edge(style="dashed") >> search_api
    auth_api >> redis
    redis >> Edge(style="dashed") >> auth_api

    # Поиск фильмов
    auth_api >> search_api
    search_api >> elastic
    elastic >> search_api
    search_api >> nginx
