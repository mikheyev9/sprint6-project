# app/core/base.py

"""Импорты класса Base и всех моделей для Alembic."""
from src.db.postgres import Base  # noqa
from src.models.film import MovieBaseDTO, MovieInfoDTO  # noqa
from src.models.genre import GenreDTO, GenresDTO  # noqa
from src.models.person import FilmDTO, PersonDTO, PersonInfoDTO  # noqa
from src.models.user_model import User  # noqa 
from src.models.mixins import UUIDMixin  # noqa 
