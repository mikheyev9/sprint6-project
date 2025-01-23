from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field

from models.person import Person, PersonFilm
from services.person import PersonService, get_person_service


router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='person not found'
        )
    return person


@router.get('/search/', response_model=list[Person])
async def search_person(
    page_number: Optional[int] = Field(50, ge=1),
    page_size: Optional[int] = Field(1, ge=1),
    query: str = Field(min_length=1, max_length=100),
    person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
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


@router.get('/{person_id}/film', response_model=list[PersonFilm])
async def get_films(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> list[PersonFilm]:
    films = await person_service.get_by_person(person_id)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='films not found'
        )
    return films
