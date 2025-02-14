from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request, Response

from models.person import PersonInfoDTO
from models.film import MovieBaseDTO
from services.film_service import FilmService, get_film_service
from services.person_service import PersonService, get_person_service
from fastapi_cache.decorator import cache

router = APIRouter()


@router.get(
    '/{person_id}',
    response_model=PersonInfoDTO,
    summary='Get person',
    description='Get person deatails.',
)
@cache(expire=60)
async def person_details(
    person_id: Annotated[
        str,
        Path(
            title="person id",
            description="Person id for the item to search in the database",
        ),
    ],
    request: Request,
    response: Response,
    person_service: PersonService = Depends(get_person_service),
) -> PersonInfoDTO:
    return await person_service.get_by_id(person_id)


@router.get(
    '/search/',
    response_model=list[PersonInfoDTO],
    summary='Get persons from search',
    description='Get persons from search with sort and pagination.',
)
@cache(expire=60)
async def search_person(
    request: Request,
    response: Response,
    page_size: Annotated[
        int,
        Query(
            title="page size",
            description="Page size for count of items to response",
            gt=0,
        )
    ] = 50,
    page_number: Annotated[
        int,
        Query(
            title="page number",
            description="Page number for count of items to response",
            gt=0,
        )
    ] = 1,
    query: Annotated[
        str,
        Query(
            title="search words",
            description="Words for search of items in the database",
        )
    ] = None,
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonInfoDTO]:
    return await person_service.search(
        page_number=page_number,
        page_size=page_size,
        full_name=query,
    )


@router.get(
    '/{person_id}/film',
    response_model=list[MovieBaseDTO],
    summary='Get films of person',
    description='Get films of person with parameters of model Movie.',
)
@cache(expire=60)
async def get_films(
    request: Request,
    response: Response,
    person_id: Annotated[
        str,
        Path(
            title="person id",
            description="Person id for the films to search in the database",
        ),
    ],
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service)
) -> list[MovieBaseDTO]:
    person = await person_service.get_by_id(person_id)
    return [await film_service.get_by_id(film.id) for film in person.films]
