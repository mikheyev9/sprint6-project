from pydantic import BaseModel


class FilmBase(BaseModel):
    id: str
    title: str
    imdb_rating: str


class Film(FilmBase):
    pass
