from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.genre import Genre
from services.genre import GenreService, get_genre_service
from fastapi_cache.decorator import cache

router = APIRouter()


@router.get('/{genre_id}', response_model=Genre)
@cache(expire=60)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(
        genre_id=genre_id
    )
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='genre not found'
        )
    return genre


@router.get('/', response_model=list[Genre])
@cache(expire=60)
async def get_films(
    genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    genres = await genre_service.get_genres()
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='genres not found'
        )
    return genres
