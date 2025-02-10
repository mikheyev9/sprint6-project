from http import HTTPStatus
from typing import List

from fastapi import HTTPException, Depends

from db.abstract_db import AbstractDAO, get_db
from services.abc.singlton_abc import SingletonService
from models.person import PersonInfoDTO


class PersonService(SingletonService):
    def __init__(self, db: AbstractDAO = Depends(get_db)):
        self.db = db
        self.index = "persons"
    
    async def get_by_id(self, entity_id: str):
        """
        Получает объект по ID.
        """
        
        doc = await self.db.get(table=self.index, id_obj=entity_id)
        
        if not doc:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'persons not found',
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