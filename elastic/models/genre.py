from pydantic import Field
from .mixins import UUIDMixin


class GenreDTO(UUIDMixin):
    """Модель жанров"""
    name: str = Field(default_factory=str)


# Через obj connect запрашиваем эластик(логика с redis) и 
# получая данные мы выладируем их с помощью pydantic 
# и отдаем response