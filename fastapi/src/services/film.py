import logging
from typing import List, Optional

from db.abstract_db import AbstractDB
from services.base_service import BaseService
from models.film import MovieInfoDTO, MovieBaseDTO

logger = logging.getLogger(__name__)


class FilmService(BaseService[MovieInfoDTO]):
    service_name = 'film'

    def __init__(self, search_db: AbstractDB):
        super().__init__(search_db, index="movies", model=MovieInfoDTO)

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

        search_query = {"bool": {}}
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
            search_query["bool"]["must"] = must_conditions

        if filter_conditions:
            search_query["bool"]["filter"] = filter_conditions

        response = await self.search_db.search(
            table=self.index,
            query=search_query,
            offset=(page_number - 1) * page_size,
            limit=page_size,
            sort=[{sort: "desc"}],
        )
        return [
            MovieBaseDTO(
                **hit["_source"]
            ) for hit in response["hits"]["hits"]
        ]
