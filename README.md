# Сервис ETL

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=Docker)](https://www.docker.com/)
[![Elasticsearch](https://img.shields.io/badge/-Elasticsearch-464646?style=flat-square&logo=elasticsearch)](https://www.elastic.co/elasticsearch/)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)](https://redis.io/)

## Описание
Данный ETL-сервис предназначен для загрузки данных о фильмах в Elasticsearch. Он обеспечивает надежное и эффективное управление данными, а также включает механизмы обработки ошибок и хранения состояния.


### Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone <URL_репозитория>
   cd <папка_проекта>

2. Создать .env на основе .env.template
    ```bash
    cp .env.template .env

3. Собрать контейнеры
    ```bash
    docker-compose up --build -d

------------

## Запуск тестов

1. Создайте файл .env для тестов
   ```bash
   cp /tests/.env.example /tests/.env

1. Запустите тестовое окружение в Docker
   ```bash
   docker compose -f docker-compose-test.yml up --build

