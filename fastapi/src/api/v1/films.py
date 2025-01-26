from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.models.film import MovieInfoDTO, MovieBaseDTO
from src.services.film import FilmService, get_film_service


router = APIRouter()


@router.get('/{film_id}', response_model=MovieInfoDTO)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> MovieInfoDTO:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='film not found'
        )
    return film


@router.get('/', response_model=list[MovieBaseDTO])
async def get_films(
    genre: str | None = None,
    page_size: Annotated[int, Query(gt=0)] = 50,
    page_number: Annotated[int, Query(gt=0)] = 1,
    sort: Annotated[str, Query()] = 'imdb_rating',
    film_service: FilmService = Depends(get_film_service)
 ) -> list[MovieBaseDTO]:
    films = await film_service.get_films(
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


@router.get('/search/', response_model=list[MovieBaseDTO])
async def search_films(
    page_size: Annotated[int, Query(gt=0)] = 50,
    page_number: Annotated[int, Query(gt=0)] = 1,
    query: Annotated[str, Query()] = None,
    film_service: FilmService = Depends(get_film_service)
) -> list[MovieBaseDTO]:
    films = await film_service.get_films(
        page_number=page_number,
        page_size=page_size,
        query=query,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='films not found'
        )
    return films
