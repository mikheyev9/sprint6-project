from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response


from models.film import MovieInfoDTO, MovieBaseDTO
from services.film import FilmService
from services.service_factory import service_for
from fastapi_cache.decorator import cache

router = APIRouter()


@cache(expire=60)
@router.get('/', response_model=list[MovieBaseDTO])
async def get_films(
    request: Request,
    response: Response, 
    genre: str | None = None,
    page_size: Annotated[int, Query(gt=0)] = 50,
    page_number: Annotated[int, Query(gt=0)] = 1,
    sort: Annotated[str, Query()] = 'imdb_rating',
    film_service: FilmService = Depends(service_for("film"))
 ) -> list[MovieBaseDTO]:
    films = await film_service.search(
        genre=genre,
        page_number=page_number,
        page_size=page_size,
        sort=sort
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='films not found'
        )
    return films


@cache(expire=60, )
@router.get('/{film_id}', response_model=MovieInfoDTO)
async def film_details(
    request: Request,
    response: Response, 
    film_id: str,
    film_service: FilmService = Depends(service_for("film"))
) -> MovieInfoDTO:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='film not found'
        )
    return film



@cache(expire=60)
@router.get('/search/', response_model=list[MovieBaseDTO])
async def search_films(
    request: Request,
    response: Response, 
    page_size: Annotated[int, Query(gt=0)] = 50,
    page_number: Annotated[int, Query(gt=0)] = 1,
    query: Annotated[str, Query()] = None,
    film_service: FilmService = Depends(service_for("film"))
) -> list[MovieBaseDTO]:
    films = await film_service.search(
        page_number=page_number,
        page_size=page_size,
        query=query,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='films not found'
        )
    return films
