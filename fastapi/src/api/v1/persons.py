from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response

from models.person import PersonInfoDTO
from models.film import MovieBaseDTO
from services.film import FilmService
from services.person import PersonService
from services.service_factory import service_for
from fastapi_cache.decorator import cache

router = APIRouter()


@router.get('/{person_id}', response_model=PersonInfoDTO)
@cache(expire=60)
async def person_details(
    person_id: str,
    request: Request,
    response: Response,
    person_service: PersonService = Depends(service_for("person")),
) -> PersonInfoDTO:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='person not found'
        )
    return person


@router.get('/search/', response_model=list[PersonInfoDTO])
@cache(expire=60)
async def search_person(
    request: Request,
    response: Response,
    page_size: Annotated[int, Query(gt=0)] = 50,
    page_number: Annotated[int, Query(gt=0)] = 1,
    query: Annotated[str, Query()] = None,
    person_service: PersonService = Depends(service_for("person")),
) -> list[PersonInfoDTO]:
    persons = await person_service.search(
        page_number=page_number,
        page_size=page_size,
        full_name=query,
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='persons not found'
        )
    return persons


@router.get('/{person_id}/film', response_model=list[MovieBaseDTO])
@cache(expire=60)
async def get_films(
    request: Request,
    response: Response,
    person_id: str,
    person_service: PersonService = Depends(service_for("person")),
    film_service: FilmService = Depends(service_for("film"))
) -> list[MovieBaseDTO]:
    person = await person_service.get_by_id(person_id)

    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='person not found'
        )
    return [await film_service.get_by_id(film.id) for film in person.films]
