from src.api.v1 import films_router, genres_router, persons_router, role_router, user_router

from fastapi import APIRouter

API_V1: str = "/api/v1"
main_router = APIRouter()
main_router.include_router(films_router, prefix=f"{API_V1}/films", tags=["films"])
main_router.include_router(genres_router, prefix=f"{API_V1}/genres", tags=["genres"])
main_router.include_router(persons_router, prefix=f"{API_V1}/persons", tags=["persons"])
main_router.include_router(user_router)
main_router.include_router(role_router, prefix=f"{API_V1}/roles", tags=["roles"])
