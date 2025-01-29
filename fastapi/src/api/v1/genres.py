from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from models.genre import GenreDTO
from services.genre import GenreService
from services.service_factory import service_for
from fastapi_cache.decorator import cache


router = APIRouter()


@cache(expire=60)
@router.get('/', response_model=List[GenreDTO])
async def get_films(
    request: Request,
    response: Response,
    genre_service: GenreService = Depends(service_for("genre"))
) -> List[GenreDTO]:
    genres = await genre_service.search()
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='genres not found'
        )
    return genres


@cache(expire=60)
@router.get('/{genre_id}', response_model=GenreDTO)
async def genre_details(
    request: Request,
    response: Response,
    genre_id: str,
    genre_service: GenreService = Depends(service_for("genre"))
) -> GenreDTO:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='genre not found'
        )
    return genre
