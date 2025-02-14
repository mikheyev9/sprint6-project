from dataclasses import dataclass
from http import HTTPStatus
from functools import lru_cache
from typing import List

from fastapi import HTTPException, Depends

from db.abstract_db import AbstractDAO, get_db
from models.person import PersonInfoDTO


@lru_cache()
def get_person_service(
    db: AbstractDAO = Depends(get_db),
) -> 'PersonService':
    return PersonService(db)

@dataclass
class PersonService:
    """Сервис для работы с персонами."""
    db: AbstractDAO
    index: str = "persons"
    
    async def get_by_id(self, entity_id: str):
        """
        Получает объект по ID.
        """
        
        doc = await self.db.get(table=self.index, id_obj=entity_id)
        
        if not doc:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'{self.index} not found',
            )
        return PersonInfoDTO(**doc)

    async def search(
        self,
        page_size: int = 50,
        page_number: int = 1,
        full_name: str | None = None
    ) -> List[PersonInfoDTO]:
        """
        Выполняет поиск персон по имени.
        """
        
        filters = {}
        
        if full_name:
            filters["full_name"] = full_name
            
        response = await self.db.search(
            table=self.index,
            offset=(page_number - 1) * page_size,
            limit=page_size,
            filters=filters,
        )
        
        if not response:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='persons not found'
            )
            
        return [PersonInfoDTO(**hit) for hit in response]