from http import HTTPStatus
from typing import List

from fastapi import HTTPException, Depends

from db.abstract_db import AbstractDAO, get_db
from services.abc.singlton_abc import SingletonService
from models.genre import GenreDTO

class GenreService(SingletonService):
    def __init__(self, db: AbstractDAO = Depends(get_db)):
        self.db = db
        self.index = "genres"

    
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