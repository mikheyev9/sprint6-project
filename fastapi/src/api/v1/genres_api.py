from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, Request, Response

from models.genre import GenreDTO
from services.genre_service import GenreService, get_genre_service
from fastapi_cache.decorator import cache
from fastapi import Query


router = APIRouter()


@router.get(
    '/',
    response_model=List[GenreDTO],
    summary='Get genres',
    description='Get all genres.',
)
@cache(expire=60)
async def get_genres(
    request: Request,
    response: Response,
    genre_service: GenreService = Depends(get_genre_service),
    page_number: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1),
) -> List[GenreDTO]:
    return await genre_service.search(page_number=page_number, page_size=page_size)


@router.get(
    '/{genre_id}',
    response_model=GenreDTO,
    summary='Get genre',
    description='Get genre details.',
)
@cache(expire=60)
async def genre_details(
    request: Request,
    response: Response,
    genre_id: Annotated[
        str,
        Path(
            title="genre id",
            description="Genre id for the item to search in the database",
        ),
    ],
    genre_service: GenreService = Depends(get_genre_service)
) -> GenreDTO:
    return await genre_service.get_by_id(genre_id)
