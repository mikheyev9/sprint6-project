import logging

import pytest
import time
from http import HTTPStatus


logger = logging.getLogger(__name__)

from functional.testdata.es_generate import GENRES_DATA


@pytest.mark.asyncio
async def test_get_all_genres(make_get_request):
    """
    Проверяет, что без параметров эндпоинт /genres возвращает все жанры.
    """
    
    endpoint = "genres"
    status, body, _ = await make_get_request(endpoint)

    assert status == HTTPStatus.OK, f"Ожидался статус 200, получили {status}"
    assert isinstance(body, list), "Ожидаем получить список жанров."
    assert len(body) > 0, "Список жанров не должен быть пустым"
    
    first_genre = body[0]
    assert "id" in first_genre, "У жанра должен быть ключ 'id'"
    assert "name" in first_genre, "У жанра должен быть ключ 'name'"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "genre_id, expected_status",
    [
        (genre["id"], HTTPStatus.OK) for genre in GENRES_DATA["genres"]
    ] + [("nonexistent-genre-id", HTTPStatus.NOT_FOUND)]
)
async def test_get_genre_by_id(make_get_request, genre_id, expected_status):
    """
    Проверяет, что запрос конкретного жанра по ID:
    - При валидном ID -> статус 200 и корректная структура
    - При невалидном или несуществующем ID -> статус 404
    """
    endpoint = f"genres/{genre_id}"
    status, body, _ = await make_get_request(endpoint)

    assert status == expected_status, (
        f"Для genre_id={genre_id} ожидался статус {expected_status}, "
        f"но получили {status}"
    )

    if status == HTTPStatus.OK:
        expected_genre = next(
            (genre for genre in GENRES_DATA["genres"] if genre["id"] == genre_id),
            None
        )
        assert expected_genre, f"Жанр с ID {genre_id} не найден в тестовых данных."
        assert "id" in body and "name" in body, "Ответ должен содержать 'id' и 'name'."
        assert body["id"] == expected_genre["id"], "ID жанра в ответе не совпадает с запрошенным."
        assert body["name"] == expected_genre["name"], "Название жанра не совпадает с ожидаемым."


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query_params, expected_status",
    [
        ({"page_number": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"page_size": 0}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"page_number": "abc"}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ]
)
async def test_genre_validation(make_get_request, query_params, expected_status):
    """
    Проверяет граничные случаи по валидации:
    - Неотрицательный page_number
    - Неотрицательный page_size
    - Допустимые типы данных
    """
    
    endpoint = "genres"
    status, body, _ = await make_get_request(endpoint, query_params)

    assert status == expected_status, (
        f"Ожидался статус {expected_status} при передаче параметров {query_params}, "
        f"но получили {status}"
    )


@pytest.mark.asyncio
async def test_genre_redis_caching(redis_clean, make_get_request, redis_client):
    """
    Проверка кеширования в Redis:
    1. Очищаем Redis
    2. Делаем запрос к /genres
    3. Проверяем, что ключ появился в Redis
    4. Делаем повторный запрос (опционально проверяем время/логику)
    """
    
    await redis_clean()
    count_keys_before = await redis_client.dbsize()
    assert count_keys_before == 0, "Redis должен быть пуст перед тестом кеширования."

    endpoint = "genres"
    status_first, body_first, _ = await make_get_request(endpoint)
    assert status_first == HTTPStatus.OK, "Первый запрос должен вернуть 200"

    count_keys_after = await redis_client.dbsize()
    assert count_keys_after > 0, (
        "Ожидалось, что после первого запроса в Redis появятся ключи (кэш)."
    )

    t_start = time.time()
    status_second, body_second, _ = await make_get_request(endpoint)
    t_finish = time.time()

    assert status_second == HTTPStatus.OK, "Второй запрос должен вернуть 200"
    assert body_first == body_second, "Ответ при втором запросе должен совпадать с первым (кэш)"

    # Опционально проверяем время — если у вас очень быстрый сервис, может быть, разница будет не особо заметна
    elapsed = t_finish - t_start
    logger.info(f"Время выполнения второго запроса: {elapsed} сек")
    # Тут можно делать какую-то логику, мол, если первый запрос был 0.2 c, а второй 0.05 c, значит кэш отработал

