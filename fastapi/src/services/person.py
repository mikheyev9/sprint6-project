from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonFilm


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    #Прописать получение по параметрам поиска
    async def get_persons(
        self,
        page_size: int = 50,
        page_number: int = 1,
        query: str = None

    ) -> Optional[list[Person]]:
        pass

    #Прописать получение персоны
    async def get_by_id(self, person_id: str) -> Optional[Person]:
        pass

    #Прописать получение фильмов по персоне
    async def get_by_person(
        self,
        person_id: str
    ) -> Optional[list[PersonFilm]]:
        pass


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
