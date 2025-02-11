from dataclasses import dataclass
from http import HTTPStatus
from typing import List
from functools import lru_cache


from fastapi import HTTPException, Depends

from db.abstract_db import AbstractDAO, get_db
from models.genre import GenreDTO


@lru_cache()
def get_genre_service(
    db: AbstractDAO = Depends(get_db),
) -> 'GenreService':
    return GenreService(db)

@dataclass
class GenreService:
    """Сервис для работы с жанрами."""
    db: AbstractDAO
    index: str = "genres"

    async def get_by_id(self, entity_id: str):
        """
        Получает жанр по ID.
        """
        
        doc = await self.db.get(table=self.index, id_obj=entity_id)
        
        if not doc:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'genres not found',
            )
        return GenreDTO(**doc)

    async def search(self, page_size: int = 50) -> List[GenreDTO]:
        """
        Возвращает список всех жанров.
        """
        
        response = await self.db.search(
            table=self.index,
            limit=page_size,
        )
        
        if not response:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='genres not found'
            )
            
        return [GenreDTO(**hit) for hit in response]