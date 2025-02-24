from fastapi import APIRouter

from src.api.v1 import films_router, genres_router, persons_router, user_router


main_router = APIRouter()
main_router.include_router(films_router, prefix="/api/v1/films", tags=["films"])
main_router.include_router(genres_router, prefix="/api/v1/genres", tags=["genres"])
main_router.include_router(persons_router, prefix="/api/v1/persons", tags=["persons"])
main_router.include_router(user_router)
