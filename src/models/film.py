from .genre import Genre
from .mixins import MovieMixin
from .person import Person


class Film(MovieMixin):
    title: str
    description: str
    imdb_rating: float
    genre: list[Genre]
    director: list[Person] | None = []
    actors: list[Person]
    writers: list[Person]
