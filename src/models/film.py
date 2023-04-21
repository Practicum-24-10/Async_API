from src.models.genre import Genre
from src.models.mixins import MovieMixin
from src.models.person import Person


class Film(MovieMixin):
    title: str
    description: str
    imdb_rating: float
    genre: list[Genre]
    director: list[Person] | None = []
    actors: list[Person]
    writers: list[Person]
