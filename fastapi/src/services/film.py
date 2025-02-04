import logging
from typing import List, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError, TransportError

from services.base_service import BaseService
from models.film import MovieInfoDTO, MovieBaseDTO

logger = logging.getLogger(__name__)


class FilmService(BaseService[MovieInfoDTO]):
    service_name = 'film'

    def __init__(self, elastic: AsyncElasticsearch):
        super().__init__(elastic, index="movies", model=MovieInfoDTO)

    async def search(
        self,
        genre: Optional[str] = None,
        page_size: int = 50,
        page_number: int = 1,
        sort: str = "imdb_rating",
        query: Optional[str] = None
    ) -> List[MovieBaseDTO]:
        """
        Получает список фильмов из Elasticsearch
        с поддержкой фильтрации, сортировки и пагинации.
        """

        search_query = {
            "size": page_size,
            "from": (page_number - 1) * page_size,
            "sort": [{sort: "desc"}],
            "query": {"bool": {}}
        }

        must_conditions = []
        filter_conditions = []

        if genre:
            filter_conditions.append({
                "nested": {
                    "path": "genre", "query": {
                        "bool": {"must": [{"match": {"genre.name": genre}}]}
                    }
                }
            })

        if query:
            must_conditions.append({
                "multi_match": {
                    "query": query,
                    "fields": [
                        "title",
                    ]
                }
            })

        if must_conditions:
            search_query["query"]["bool"]["must"] = must_conditions

        if filter_conditions:
            search_query["query"]["bool"]["filter"] = filter_conditions

        try:
            response = await self.elastic.search(
                index=self.index,
                body=search_query
            )
            return [
                MovieBaseDTO(
                    **hit["_source"]
                ) for hit in response["hits"]["hits"]
            ]

        except NotFoundError:
            logger.warning(f"Фильмы не найдены: genre={genre}, query={query}")
            return []

        except TransportError as e:
            logger.error(f"Ошибка запроса к Elasticsearch: {e}")
            return []
