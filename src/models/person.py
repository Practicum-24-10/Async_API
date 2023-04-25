from pydantic import BaseModel

from src.models.mixins import MovieMixin


class PersonFilmES(MovieMixin):
    title: str
    imdb_rating: float


class FilmPersonES(MovieMixin):
    roles: list[str]


class ListPersonFilm(BaseModel):
    films: list[PersonFilmES]


class PersonES(MovieMixin):
    full_name: str
    films: list[FilmPersonES]


class SearchPersons(BaseModel):
    items: list[PersonES]

class Person(MovieMixin):
    full_name: str
    
    