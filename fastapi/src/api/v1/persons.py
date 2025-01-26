from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.models.person import PersonInfoDTO, PersonsDTO
from src.models.film import MovieBaseDTO
from src.services.person import PersonService, get_person_service


router = APIRouter()


@router.get('/{person_id}', response_model=PersonInfoDTO)
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> PersonInfoDTO:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='person not found'
        )
    return person


@router.get('/search/', response_model=PersonsDTO)
async def search_person(
    page_size: Annotated[int, Query(gt=0)] = 50,
    page_number: Annotated[int, Query(gt=0)] = 1,
    query: Annotated[str, Query()] = None,
    person_service: PersonService = Depends(get_person_service)
) -> PersonsDTO:
    persons = await person_service.get_persons(
        page_number=page_number,
        page_size=page_size,
        query=query,
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='persons not found'
        )
    return persons


@router.get('/{person_id}/film', response_model=list[MovieBaseDTO])
async def get_films(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
) -> list[MovieBaseDTO]:
    films = await person_service.get_by_person(person_id)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='films not found'
        )
    return films