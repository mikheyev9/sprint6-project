from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field

from models.film import Film, FilmBase
from services.film import FilmService, get_film_service


router = APIRouter()


@router.get('/{film_id}', response_model=Film)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='film not found'
        )
    return film


@router.get('/', response_model=list[FilmBase])
async def get_films(
    genre: Optional[str] = None,
    page_number: Optional[int] = Field(50, ge=1),
    page_size: Optional[int] = Field(1, ge=1),
    sort: Optional[str] = 'imdb_rating',
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmBase]:
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


@router.get('/search/', response_model=list[FilmBase])
async def search_films(
    page_number: Optional[int] = Field(50, ge=1),
    page_size: Optional[int] = Field(1, ge=1),
    query: str = Field(min_length=1, max_length=100),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmBase]:
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
